import numpy as np
import pytest
from src.betteredit.config import ColorDetectionConfig
from src.analyzer.features.color_detection.base import ColorDetector

@pytest.fixture
def dummy_cfg():
    return ColorDetectionConfig(
        salience_strategy="weighted",
        contrast_method="combined",
        sobel_weight=0.5,
        rarity_space="lab",
        rarity_k=4,
        weights={"hue":0.1,"sat":0.3,"rarity":0.2,"lum":0.4},
        return_density=True,
        return_salience=True,
        density_window_size=4
    )

def test_detect_color_outputs(dummy_cfg):
    # synthetic BGR image
    img = np.zeros((8,8,3),dtype=np.uint8)
    image_data = {
        "bgr": {"og": img},
    }
    cd = ColorDetector(dummy_cfg)
    result = cd.detect(image_data)
    # Should have cues for hue, saturation, luminance, rarity, hue_contrast, luminance_contrast
    expected = {"hue","saturation","luminance","rarity","hue_contrast","luminance_contrast"}
    assert set(result["cues"].keys()) >= expected
    # Combined block
    assert "strength" in result["combined"]