#!/usr/bin/env python3
"""
betteredit CLI

This module provides command-line interface for the betteredit,
combining both single image analysis and benchmarking functionality.
"""

import os
import sys
import yaml
import uuid
import json
import argparse
import numpy as np
from loguru import logger
from typing import Dict, Any, Tuple, Optional

# Add project root to path
BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASEDIR not in sys.path:
    sys.path.insert(0, BASEDIR)

from src.betteredit.config import Settings
from src.pipeline import main as pipeline_main
from src.config.design_registry import DesignRegistry
from src.analyzer.preprocessing import preprocess_image
from src.analyzer.features.base import FeatureExtractor
from src.analyzer.report.report_generator import *

# Default paths
DEFAULT_CONFIG_PATH = os.path.join(BASEDIR, "src", "betteredit", "config", "settings.yaml")
BENCHMARK_INPUT_DIR = os.path.join(BASEDIR, "benchmarking", "image_set")
BENCHMARK_OUTPUT_DIR = os.path.join(BASEDIR, "outputs", "benchmarking")
ANALYSIS_OUTPUT_DIR = os.path.join(BASEDIR, "outputs", "analysis")
STRATEGIES = ["minimal", "boosted", "full", "sum", "weighted"]


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle NumPy arrays and other non-serializable objects."""
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        return super().default(obj)


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge override into base."""
    merged = base.copy()
    for key, val in override.items():
        if (
            key in merged
            and isinstance(merged[key], dict)
            and isinstance(val, dict)
        ):
            merged[key] = deep_merge(merged[key], val)
        else:
            merged[key] = val
    return merged


def load_settings(
    config_path: Optional[str] = None,
    image_path: Optional[str] = None,
    output_dir: Optional[str] = None
) -> Settings:
    """
    Load and merge settings from base config, user config, and CLI overrides.
    """
    # Load base config
    if not os.path.isfile(DEFAULT_CONFIG_PATH):
        raise FileNotFoundError(f"Default config not found: {DEFAULT_CONFIG_PATH}")
    
    with open(DEFAULT_CONFIG_PATH, "r") as f:
        base_cfg_dict = yaml.safe_load(f)

    # Merge user config if provided
    if config_path:
        if not os.path.isfile(config_path):
            raise FileNotFoundError(f"User config not found: {config_path}")
        with open(config_path, "r") as f:
            override_cfg_dict = yaml.safe_load(f)
        merged_cfg_dict = deep_merge(base_cfg_dict, override_cfg_dict)
    else:
        merged_cfg_dict = base_cfg_dict

    # Apply CLI overrides
    if image_path:
        merged_cfg_dict["image_path"] = image_path
    if output_dir:
        merged_cfg_dict["output_dir"] = output_dir

    # Instantiate Settings
    try:
        cfg = Settings(**merged_cfg_dict)
    except Exception as e:
        logger.error("Failed parsing Settings from merged config: %r", merged_cfg_dict)
        raise

    return cfg


def setup_logging():
    """Configure logging for CLI operations."""
    logger.remove()
    logger.add(
        sys.stderr,
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} [{level}] {message}"
    )
    session_id = uuid.uuid4()
    bound_logger = logger.bind(session_id=session_id)
    globals()["logger"] = bound_logger
    return str(session_id)


def process_single_image(cfg: Settings):
    """Process a single image through the analysis pipeline."""
    logger.info("Running analysis on: %s", cfg.image_path)
    
    # Sanity checks
    if not os.path.isfile(cfg.image_path):
        raise FileNotFoundError(f"Image file not found: {cfg.image_path}")
    
    if cfg.output_dir is None:
        raise ValueError("No output_dir specified. Please set `output_dir:` in your YAML or pass `--output-dir`.")
    
    os.makedirs(cfg.output_dir, exist_ok=True)
    
    # Run pipeline
    results = pipeline_main(cfg)
    logger.info("Analysis completed successfully")
    return results


def process_benchmark_image(img_path: str, target_size: Tuple[int, int], cfg: Settings, output_dir: str):
    """Process a single image for benchmarking across multiple strategies."""
    img_name = os.path.splitext(os.path.basename(img_path))[0]
    logger.info(f"\n[IMAGE] Processing: {img_name}")
    
    image_data = preprocess_image(img_path, target_size)
    report: Dict[str, Any] = {}

    for strategy in STRATEGIES:
        # Build per-strategy config objects
        color_cfg = cfg.color_detection.model_copy(update={"salience_strategy": strategy})
        edge_cfg = cfg.edge_detection

        # Instantiate extractor
        extractor = FeatureExtractor(
            enable_color=True,
            enable_edges=True,
            enable_objects=False,
            enable_saliency=False,
            use_dl_models=False,
            color_detector_config=color_cfg,
            edge_detector_config=edge_cfg
        )

        # Run extraction
        features = extractor.extract(image_data)
        color = features.get("color", {})

        # Register benchmark results
        DesignRegistry.register(
            module="Benchmarking",
            component="Strategy Comparison",
            concept="Strategy Run",
            technique=strategy,
            tuning_params={
                "image_name": img_name,
                "strategy": strategy,
                "color_salience_strategy": color_cfg.salience_strategy,
                "edge_intra_fusion_strategy": edge_cfg.intra_fusion_strategy,
                "features_extracted": list(features.keys())
            }
        )

        # Process results
        report[strategy] = {}
        for feature_name, feature_data in color.items():
            if isinstance(feature_data, dict) and "map" in feature_data:
                map_data = feature_data["map"]
                if map_data is not None:
                    stats = summarize_stats(map_data)
                    report[strategy][feature_name] = stats
                    log_stats(img_name, strategy, stats)

                    # Save visualizations
                    output_path = os.path.join(
                        output_dir, f"{img_name}_{strategy}_{feature_name}.png"
                    )
                    save_visual_map(
                        feature_map=map_data,
                        output_path=output_path,
                        title=f"{feature_name} ({strategy})",
                        cmap="viridis",
                        save_visuals=True
                    )

    # Save report
    report_path = os.path.join(output_dir, f"{img_name}_benchmark_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2, cls=NumpyEncoder)
    logger.info(f"[SAVED] Benchmark report: {report_path}")


def run_benchmark(cfg: Settings, target_size: Tuple[int, int], input_dir: str, output_dir: str):
    """Run benchmarking across all images in the input directory."""
    logger.info(f"Starting benchmark with target size: {target_size}")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Register benchmark session
    DesignRegistry.register(
        module="Benchmarking",
        component="Session",
        concept="Benchmark Start",
        technique="multi_strategy_comparison",
        tuning_params={
            "target_size": target_size,
            "strategies": STRATEGIES,
            "input_dir": input_dir,
            "output_dir": output_dir
        }
    )

    # Process each image
    image_count = 0
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(input_dir, filename)
            process_benchmark_image(img_path, target_size, cfg, output_dir)
            image_count += 1

    # Register benchmark completion
    DesignRegistry.register(
        module="Benchmarking",
        component="Session",
        concept="Benchmark Complete",
        technique="multi_strategy_comparison",
        tuning_params={
            "images_processed": image_count
        }
    )
    
    # Write registry
    DesignRegistry.to_json(os.path.join(output_dir, "benchmark_design_registry.json"))
    logger.info("Benchmark completed successfully")


def main():
    parser = argparse.ArgumentParser(description="betteredit CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a single image and export a JSON summary.",
        description="Analyze a single image for visual composition and salience."
    )
    analyze_parser.add_argument("--image", required=True, help="Path to input image file.")
    analyze_parser.add_argument("--config", required=False, help="Path to YAML config file.")
    analyze_parser.add_argument("--output-dir", required=False, default=ANALYSIS_OUTPUT_DIR, help="Directory to write outputs.")

    # Benchmark command
    benchmark_parser = subparsers.add_parser(
        "benchmark",
        help="Benchmark a set of images and export reports.",
        description="Benchmark a set of images across multiple strategies."
    )
    benchmark_parser.add_argument("--input-dir", required=False, default=BENCHMARK_INPUT_DIR, help="Directory of images to benchmark.")
    benchmark_parser.add_argument("--config", required=False, help="Path to YAML config file.")
    benchmark_parser.add_argument("--output-dir", required=False, default=BENCHMARK_OUTPUT_DIR, help="Directory to write outputs.")
    benchmark_parser.add_argument("--target-size", required=False, default="512,224", help="Target size as W,H (e.g., 512,224)")

    args = parser.parse_args()

    # Setup logging and session
    session_id = setup_logging()

    try:
        if args.command == "analyze":
            cfg = load_settings(
                config_path=args.config,
                image_path=args.image,
                output_dir=args.output_dir
            )
            DesignRegistry.start_session(session_id, cfg.model_dump())

            # NEW: Set up analysis-specific output directories
            if args.output_dir:
                # User provided output directory
                analysis_output_dir = args.output_dir
            else:
                # Default to outputs/analysis
                analysis_output_dir = ANALYSIS_OUTPUT_DIR
            
            # Create analysis subdirectories
            color_output_dir = os.path.join(analysis_output_dir, "color_detection")
            edge_output_dir = os.path.join(analysis_output_dir, "edge_detection")
            
            os.makedirs(color_output_dir, exist_ok=True)
            os.makedirs(edge_output_dir, exist_ok=True)
            
            # Update config with the new output directories
            cfg.output_dir = analysis_output_dir
            
            # Debug: Check what output_dir we have
            logger.info(f"Output directory: {cfg.output_dir}")
            logger.info(f"Color output directory: {color_output_dir}")
            logger.info(f"Edge output directory: {edge_output_dir}")
                
            # Create output directory if it doesn't exist
            os.makedirs(cfg.output_dir, exist_ok=True)
            logger.info(f"Created/verified output directory: {cfg.output_dir}")
            
            results = process_single_image(cfg)
            # output_path = os.path.join(cfg.output_dir, "results.json")
            # logger.info(f"Writing results to: {output_path}")
            # with open(output_path, "w") as f:
            #     json.dump(results, f, indent=2, cls=NumpyEncoder)
            # # NEW: Write analysis-specific registry
            registry_path = os.path.join(cfg.output_dir, "analysis_design_registry.json")
            DesignRegistry.to_json(registry_path)
            
            # logger.info(f"[ANALYZE] Results written to {output_path}")
            logger.info(f"[ANALYZE] Registry written to {registry_path}")


        elif args.command == "benchmark":
            # Parse target size
            try:
                w, h = map(int, args.target_size.split(","))
                target_size = (w, h)
            except ValueError:
                logger.error("TARGET_SIZE must be 'W,H' format, got: %s", args.target_size)
                sys.exit(1)

            cfg = load_settings(
                config_path=args.config,
                output_dir=args.output_dir
            )
            DesignRegistry.start_session(session_id, cfg.model_dump())
            run_benchmark(cfg, target_size, args.input_dir, args.output_dir)

        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        logger.error(f"CLI failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()