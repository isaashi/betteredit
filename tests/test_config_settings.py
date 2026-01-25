import copy
import pytest
import yaml
from src.betteredit.config import ColorDetectionConfig, EdgeDetectionConfig, Settings

VALID_YAML = {
    "image_path": "foo.jpg",
    "target_size": [100, 200],
    "save_visuals": True,
    "edge_detection": {
        "methods": ["canny"],
        "canny_sigma": 0.5,
        "sobel_ksize": 3,
        "laplacian_ksize": 3,
        "piotr_model_path": "models/model.yml.gz",
        "return_density": True,
        "return_salience": False,
        "salience_strategy": "product",
        "density_window_size": 8,
        "intra_fusion_strategy": "weighted",
        "intra_fusion_weights": {"canny": 1.0}
    },
    "color_detection": {
        "salience_strategy": "weighted",
        "contrast_method": "sobel",
        "sobel_weight": 0.7,
        "rarity_space": "lab",
        "rarity_k": 5,
        "weights": {"hue":0.2,"sat":0.2,"rarity":0.3,"lum":0.3},
        "return_density": False,
        "return_salience": True,
        "density_window_size": 12
    },
    "neural_inter_fusion": {
        "enabled": False,
        "inter_fusion_strategy": "neural",
        "model_type": "attention",
        "input_dim": 256,
        "hidden_dim": 128,
        "num_heads": 4,
        "learning_rate": 0.001,
        "batch_size": 16,
        "epochs": 100,
        "model_save_path": "models/neural_inter_fusion.pth"
    }
}

def test_settings_loads_and_validates(tmp_path, monkeypatch):
    # write a temporary YAML
    f = tmp_path / "settings.yaml"
    f.write_text(yaml.dump(VALID_YAML))
    # monkeypatch the path inside Settings if needed, or load directly:
    cfg = Settings(**VALID_YAML)
    # top‐level fields
    assert cfg.image_path == "foo.jpg"
    assert tuple(cfg.target_size) == (100, 200)
    assert cfg.save_visuals is True
    # edge sub‐config
    ed: EdgeDetectionConfig = cfg.edge_detection
    assert ed.canny_sigma == 0.5
    assert ed.intra_fusion_weights["canny"] == 1.0
    # color sub‐config
    cd: ColorDetectionConfig = cfg.color_detection
    assert cd.sobel_weight == 0.7
    assert cd.return_density is False

def test_invalid_intra_fusion_weights_rejected():
    bad = copy.deepcopy(VALID_YAML)
    bad["edge_detection"]["intra_fusion_weights"] = {"canny": 0.3, "sobel": 0.3}
    with pytest.raises(ValueError):
        Settings(**bad)