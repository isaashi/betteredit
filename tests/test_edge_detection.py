import numpy as np
import pytest
from src.betteredit.config import EdgeDetectionConfig, Settings
from src.analyzer.features.edge_detection.base import EdgeDetector

@pytest.fixture
def dummy_cfg():
    return EdgeDetectionConfig(
        methods=["canny","sobel"],
        canny_sigma=0.33,
        sobel_ksize=3,
        laplacian_ksize=3,
        piotr_model_path="models/model.yml.gz",
        return_density=True,
        return_salience=True,
        salience_strategy="product",
        density_window_size=4,
        intra_fusion_strategy="average",
        intra_fusion_weights={"canny":0.5,"sobel":0.5}
    )

def test_detect_returns_expected_keys(dummy_cfg):
    # create a synthetic 10×10 RGB + gray image_data dict
    img = np.zeros((10,10,3), dtype=np.uint8)
    image_data = {
        "rgb": {"padded": img},
        "gray": {"padded": np.zeros((10,10),dtype=np.uint8)},
    }
    ed = EdgeDetector(dummy_cfg)
    result = ed.detect(image_data)
    # Should have 'cues' and 'combined'
    assert "cues" in result and "combined" in result
    # For each method in cfg.methods, cues[method] has map, density, salience
    for m in dummy_cfg.methods:
        block = result["cues"][m]
        assert set(block.keys()) == {"map","density","salience"}
    # Combined should have at least 'strength'
    assert "strength" in result["combined"]