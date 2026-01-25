# src/config/settings.py

import yaml
from typing import Dict, List, Optional, Tuple, Union
from pydantic_settings import BaseSettings
from pydantic import BaseModel, Field, field_validator
from pathlib import Path


class EdgeDetectionConfig(BaseModel):
    methods: List[str]
    canny_sigma: float = Field(..., ge=0, description="sigma for Canny edge detector")
    sobel_ksize: int = Field(..., ge=1, description="kernel size for Sobel filter")
    laplacian_ksize: int = Field(..., ge=1, description="kernel size for Laplacian filter")
    piotr_model_path: str
    return_density: bool
    return_salience: bool
    salience_strategy: str
    density_window_size: int = Field(..., ge=1)
    intra_fusion_strategy: str
    intra_fusion_weights: Dict[str, float]

    @field_validator("intra_fusion_weights")
    @classmethod
    def check_weights_sum_to_one(cls, v):
        if abs(sum(v.values()) - 1.0) > 1e-6:
            raise ValueError("intra_fusion_weights must sum to 1.0")
        return v


class ColorDetectionConfig(BaseModel):
    salience_strategy: str
    contrast_method: str
    sobel_weight: float = Field(..., ge=0, le=1)
    rarity_space: str
    rarity_k: int = Field(..., ge=1)
    weights: Dict[str, float]
    return_density: bool = True
    return_salience: bool = True
    density_window_size: int = 16
    hue_contrast_sigma: float = 1.0


class NeuralInterFusionConfig(BaseModel):
    enabled: bool
    inter_fusion_strategy: str = Field(default="neural", description="Inter-fusion strategy: 'classical' for WeightedFusion/SumFusion, 'neural' for AttentionBasedFusion")
    model_type: str
    input_dim: int = Field(..., ge=64, le=1024)
    hidden_dim: int = Field(..., ge=64, le=1024)
    num_heads: int = Field(..., ge=1, le=16)
    learning_rate: float = Field(..., ge=1e-6, le=1e-2)
    batch_size: int = Field(..., ge=1, le=128)
    epochs: int = Field(..., ge=1, le=1000)
    model_save_path: str
    
    @field_validator("inter_fusion_strategy")
    @classmethod
    def validate_inter_fusion_strategy(cls, v):
        if v not in ["classical", "neural"]:
            raise ValueError("inter_fusion_strategy must be 'classical' or 'neural'")
        return v


class Settings(BaseSettings):
    image_path: str
    target_size: Tuple[int, int]
    save_visuals: bool
    output_dir: Optional[str] = None

    edge_detection: EdgeDetectionConfig
    color_detection: ColorDetectionConfig
    neural_inter_fusion: NeuralInterFusionConfig

    @classmethod
    def load(cls, path: Optional[Union[Path, str]] = None) -> "Settings":
        # Load all settings from single settings.yaml file
        main_cfg = Path(path or __file__).parent / "settings.yaml"
        main_data = yaml.safe_load(main_cfg.read_text())
        return cls(**main_data)