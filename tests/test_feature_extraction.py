import numpy as np
import pytest
from PIL import Image
from src.betteredit.config import Settings
from src.analyzer.preprocessing import preprocess_image
from src.analyzer.features.base import FeatureExtractor
from tests.test_config_settings import VALID_YAML

@pytest.fixture
def small_cfg():
    # use minimal valid YAML dict from test_config_settings
    return Settings(**VALID_YAML)

def test_feature_extractor_roundtrip(tmp_path, small_cfg):
    # create dummy image and write to disk
    img = (np.ones((5,5,3))*127).astype(np.uint8)
    path = tmp_path/"img.png"
    Image.fromarray(img).save(path)
    # preprocess + extract
    data = preprocess_image(str(path), (5,5))
    fe = FeatureExtractor(
        enable_color=True,
        enable_edges=True,
        enable_objects=False,
        enable_saliency=False,
        use_dl_models=False,
        color_detector_config=small_cfg.color_detection,
        edge_detector_config=small_cfg.edge_detection
    )
    feats = fe.extract(data)
    assert "color" in feats and "edges" in feats
    # each should have at least one map
    assert "hue" in feats["color"]
    assert "canny" in feats["edges"]