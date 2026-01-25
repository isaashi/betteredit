import os
import pytest
from src.pipeline import main as pipeline_main
from src.betteredit.cli import run_benchmark
from src.betteredit.config import Settings


def test_pipeline_main_smoke(tmp_path):
    """Test that pipeline main function works with real image from benchmarking folder."""
    # Get image from benchmarking folder
    benchmark_image_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "benchmarking", "image_set"))
    images = [f for f in os.listdir(benchmark_image_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    if not images:
        pytest.skip("No test images found in benchmarking/image_set")
    image_path = os.path.join(benchmark_image_dir, images[0])
    
    # Load settings and modify config (don't use env var - Pydantic Settings expects JSON)
    cfg = Settings.load()
    cfg.image_path = image_path
    cfg.output_dir = str(tmp_path)
    cfg.target_size = (64, 64)  # Set directly on config object
    
    # Should complete without error
    result = pipeline_main(cfg)
    assert result is not None


def test_benchmark_smoke(tmp_path):
    """Test benchmark functionality with real images from benchmarking folder."""
    # Use benchmarking image_set as input
    benchmark_image_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "benchmarking", "image_set"))
    output_dir = str(tmp_path / "benchmark_outputs")
    
    cfg = Settings.load()
    target_size = (64, 64)  # Pass directly to run_benchmark, not via env var
    
    # Should complete without error
    run_benchmark(cfg, target_size, benchmark_image_dir, output_dir)
    assert os.path.exists(output_dir)