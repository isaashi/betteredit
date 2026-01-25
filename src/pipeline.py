# src/analyzer.py

import os
import numpy as np
from loguru import logger
from src.betteredit.config import Settings
from src.analyzer.preprocessing import preprocess_image
from src.analyzer.features.base import FeatureExtractor
from src.analyzer.features.color_detection import transforms as color_transforms
from src.config.design_registry import DesignRegistry
from src.analyzer.report.report_generator import clear_outputs_dir, save_visual_map

OUTPUT_DIR    = "outputs"
REGISTRY_PATH = os.path.join(OUTPUT_DIR, "design_registry.json")


def run(image_path: str, target_size: tuple, cfg: Settings):
    """
    Core pipeline: preprocessing → feature extraction → visualization → registry.
    """
    logger.info(f"Starting analysis on: {image_path}")
    logger.info(f"Target resize: {target_size}")

    # Use config's output directory or default
    output_dir = cfg.output_dir if cfg.output_dir is not None else "outputs"

    # Step 1: Preprocessing
    logger.info("[STEP 1] Preprocessing image…")
    image_data = preprocess_image(image_path, target_size)
    logger.info(f" - Original Aspect Ratio: {image_data['original_aspect_ratio']}")
    logger.info(f" - Applied Padding: {image_data['padding']}")
    logger.info(f" - EXIF keys: {list(image_data['exif'].keys()) if image_data['exif'] else 'None'}")

    # Step 2: Feature Extraction
    color_cfg = cfg.color_detection
    edge_cfg  = cfg.edge_detection
    save_visuals = cfg.save_visuals

    extractor = FeatureExtractor(
        enable_color=True,
        enable_edges=True,
        enable_objects=False,
        enable_saliency=False,
        use_dl_models=False,
        color_detector_config=color_cfg,
        edge_detector_config=edge_cfg
    )

    features       = extractor.extract(image_data)
    color_features = features.get("color", {})
    edge_features  = features.get("edges", {})
    basename       = os.path.splitext(os.path.basename(image_path))[0]

    # Get raw hue map
    hue_val = color_features.get("hue")
    hue_map = hue_val["map"] if isinstance(hue_val, dict) else hue_val
    if hue_map is not None and "hue_contrast" not in color_features:
        color_features["hue_contrast"] = color_transforms.compute_hue_contrast(hue_map, color_cfg.hue_contrast_sigma)

    # Get raw luminance map
    lum_val = color_features.get("luminance")
    lum_map = lum_val["map"] if isinstance(lum_val, dict) else lum_val
    if lum_map is not None and "luminance_contrast" not in color_features:
        color_features["luminance_contrast"] = color_transforms.compute_luminance_contrast(
            lum_map,
            method=color_cfg.contrast_method,
            sobel_weight=color_cfg.sobel_weight
        )

    # Step 3: Visualization
    # — Color cues & final salience —
    for name, cmap in {
        "hue": "twilight",
        "saturation": "gray",
        "luminance": "gray",
        "hue_contrast": "hot",
        "luminance_contrast": "hot",
        "rarity": "plasma",
        "salience": "inferno"
    }.items():
        output_path = os.path.join(
            output_dir, "color_detection", f"{basename}_{name}.png"
        )
        title = name.replace("_", " ").title()

        val = color_features.get(name)
        feature_map = val["map"] if isinstance(val, dict) else val
        save_visual_map(
            feature_map=feature_map,
            output_path=output_path,
            title=title,
            cmap=cmap,
            save_visuals=save_visuals
        )

    # — Individual edge cues & salience —
    key_map = {"edge_map": "map", "edge_density": "density", "edge_salience": "salience"}
    edge_methods = [m for m in edge_features.keys() if isinstance(edge_features[m], dict)]
    for method in edge_methods:
        block = edge_features.get(method, {})
        for name, cmap in {
            "edge_map": "gray",
            "edge_density": "hot",
            "edge_salience": "inferno"
        }.items():
            output_path = os.path.join(
                output_dir,
                "edge_detection",
                f"{basename}_{method}_{name}.png"
            )
            title = f"{name.replace('_', ' ').title()} ({method})"
            feature_map = block.get(key_map[name])
            save_visual_map(
                feature_map=feature_map,
                output_path=output_path,
                title=title,
                cmap=cmap,
                save_visuals=save_visuals
            )

    # — Combined edge maps —
    fused_map_keys = {
        "edge_strength": "strength",
        "edge_density": "density",
        "edge_salience": "salience"
    }
    for name, cmap in {
        "edge_strength": "gray",
        "edge_density": "hot",
        "edge_salience": "inferno"
    }.items():
        key = fused_map_keys[name]
        feature_map = edge_features.get(key)
        output_path = os.path.join(
            output_dir,
            "edge_detection",
            f"{basename}_fused_{name}.png"
        )
        title = f"{name.replace('_', ' ').title()} (fused)"
        save_visual_map(
            feature_map=feature_map,
            output_path=output_path,
            title=title,
            cmap=cmap,
            save_visuals=save_visuals
        )


    # Step 4: logger.info extracted feature summaries
    logger.info("\n[RESULT] Features extracted:")
    for section, result in features.items():
        logger.info(f" - {section}:")
        if isinstance(result, dict):
            for k, v in result.items():
                if isinstance(v, np.ndarray):
                    logger.info(f"    - {k}: shape = {v.shape}, dtype = {v.dtype}")
                else:
                    logger.info(f"    - {k}: {v}")
        else:
            logger.info(f"    - {result}")

    # Step 5: Register only the essential high-level results
    DesignRegistry.register(
        module="Pipeline",
        component="Analysis",
        concept="Complete Run",
        technique="full_pipeline",
        tuning_params={
            "image_path": image_path,
            "target_size": target_size,
            "edge_methods": edge_cfg.methods,
            "edge_intra_fusion_strategy": edge_cfg.intra_fusion_strategy,
            "edge_intra_fusion_weights": edge_cfg.intra_fusion_weights,
            "color_salience_strategy": color_cfg.salience_strategy,
            "color_weights": color_cfg.weights,
            "features_extracted": list(features.keys()),
            "save_visuals": save_visuals
        }
    )
    # DesignRegistry.pretty_print()
    # DesignRegistry.finish_session()
    # DesignRegistry.to_json(REGISTRY_PATH)

    return features


def main(cfg: Settings):
    """
    Wraps `run()` to pull params from cfg and handle outputs dir.
    """
    # Ensure clean output folders
    clear_outputs_dir(OUTPUT_DIR)

    # Dispatch to core run()
    features = run(
        image_path=cfg.image_path,
        target_size=tuple(cfg.target_size),
        cfg=cfg
    )
    return features