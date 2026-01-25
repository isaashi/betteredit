import cv2
import numpy as np
from typing import Any, Dict
from numpy.typing import NDArray
from . import extractors, transforms
from .transforms import compute_color_density
from .intra_fusion import compute_cue_salience, compute_salience
from src.betteredit.analyzer.protocols.color_detector_protocol import ColorDetectorProtocol
from src.betteredit.analyzer.protocols.detection_protocols import DetectionResult, CueBlock
from src.analyzer.report.report_generator import print_structure
from src.betteredit.config import ColorDetectionConfig
from loguru import logger


class ColorDetector(ColorDetectorProtocol):
    """
    Unified ColorDetector supporting multiple cues and intra-fusion.
    Returns a DetectionResult with `cues` and `combined` blocks.
    """
    def __init__(self, cfg: ColorDetectionConfig):
        """
        cfg: validated ColorDetectionConfig from Pydantic.
        """
        self.salience_strategy   = cfg.salience_strategy
        self.contrast_method     = cfg.contrast_method
        self.sobel_weight        = cfg.sobel_weight
        self.rarity_space        = cfg.rarity_space
        self.rarity_k            = cfg.rarity_k
        self.weights             = cfg.weights
        self.return_density      = cfg.return_density
        self.return_salience     = cfg.return_salience
        self.density_window_size = cfg.density_window_size
        self.hue_contrast_sigma  = cfg.hue_contrast_sigma

        logger.debug(
            "Initialized ColorDetector with config:\n{}",
            cfg.model_dump_json(indent=2)
        )

    def detect(self, image_data: Dict[str, Any]) -> DetectionResult:
        # Prepare raw inputs
        bgr_img = image_data["bgr"]["og"]
        hsv = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)

        # 1. Raw cues
        raw_cues: Dict[str, np.ndarray] = {
            "hue": extractors.extract_hue_map(hsv),
            "saturation": extractors.extract_saturation_map(hsv),
            "luminance": extractors.extract_luminance_map(bgr_img),
            "rarity": transforms.compute_color_rarity(
                bgr_img,
                space=self.rarity_space,
                k=self.rarity_k
            )
        }

        outputs: DetectionResult = {"cues": {}, "combined": {}}

        # Process each raw cue
        for name, cue_map in raw_cues.items():
            block: CueBlock = {"map": cue_map}
            if self.return_density:
                block["density"] = compute_color_density(
                    cue_map, window_size=self.density_window_size
                )
            if self.return_salience:
                strength = cue_map.astype(np.float32)
                density_for_sal = block.get("density", strength)
                block["salience"] = compute_cue_salience(
                    strength=strength,
                    density=density_for_sal,
                    strategy="product"
                )
            outputs["cues"][name] = block

        # 2. Derived cues (contrast maps)
        derived: Dict[str, np.ndarray] = {
            "hue_contrast": transforms.compute_hue_contrast(raw_cues["hue"], sigma=self.hue_contrast_sigma),
            "luminance_contrast": transforms.compute_luminance_contrast(
                raw_cues["luminance"],
                method=self.contrast_method,
                sobel_weight=self.sobel_weight
            )
        }
        for name, cue_map in derived.items():
            derived_block: CueBlock = {"map": cue_map}
            if self.return_density:
                derived_block["density"] = compute_color_density(
                    cue_map, window_size=self.density_window_size
                )
            if self.return_salience:
                strength = cue_map.astype(np.float32)
                density_for_sal = derived_block.get("density", strength)
                derived_block["salience"] = compute_cue_salience(
                    strength=strength,
                    density=density_for_sal,
                    strategy="product"
                )
            outputs["cues"][name] = derived_block

        # 3. Combined fused outputs
        final_sal: np.ndarray = compute_salience(
            hue_contrast=derived["hue_contrast"],
            saturation=raw_cues["saturation"],
            rarity=raw_cues["rarity"],
            luminance_contrast=derived["luminance_contrast"],
            strategy=self.salience_strategy,
            weights=self.weights
        )
        strength_map = final_sal.astype(np.float32)
        outputs["combined"]["strength"] = strength_map
        if self.return_density:
            outputs["combined"]["density"] = compute_color_density(
                strength_map, window_size=self.density_window_size
            )
        if self.return_salience:
            density_for_sal = outputs["combined"].get("density", strength_map)
            outputs["combined"]["salience"] = compute_cue_salience(
                strength=strength_map,
                density=density_for_sal,
                strategy="product"
            )

        # ─── DEBUG ─── print full nested output for inspection
        print("=== ColorDetector.detect() STRUCTURE ===")
        print_structure(outputs)
        print("=== End STRUCTURE ===")
        return outputs