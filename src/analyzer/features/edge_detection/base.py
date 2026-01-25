import numpy as np
from typing import Any, Dict
from .extractors import extract_canny, extract_piotr, extract_sobel, extract_laplacian
from .transforms import compute_edge_density, compute_edge_salience
from .intra_fusion import compute_fused_edge_map
from src.betteredit.analyzer.protocols.edge_detector_protocol import EdgeDetectorProtocol
from src.betteredit.analyzer.protocols.detection_protocols import DetectionResult, CueBlock
from src.analyzer.report.report_generator import print_structure
from src.betteredit.config import EdgeDetectionConfig, Settings


class EdgeDetector(EdgeDetectorProtocol):
    """
    Unified EdgeDetector supporting multiple methods and intra-fusion.
    Returns a DetectionResult with `cues` and `combined` blocks.
    """
    def __init__(self, cfg: EdgeDetectionConfig):
        """
        cfg: validated EdgeDetectionConfig from Pydantic.
        """
        self.methods             = cfg.methods
        self.canny_sigma         = cfg.canny_sigma
        self.sobel_ksize         = cfg.sobel_ksize
        self.laplacian_ksize     = cfg.laplacian_ksize
        self.piotr_model_path    = cfg.piotr_model_path
        self.return_density      = cfg.return_density
        self.return_salience     = cfg.return_salience
        self.salience_strategy   = cfg.salience_strategy
        self.density_window_size = cfg.density_window_size
        self.intra_fusion_strategy     = cfg.intra_fusion_strategy
        self.intra_fusion_weights      = cfg.intra_fusion_weights


    def detect(self, image_data: Dict[str, Any]) -> DetectionResult:
        # Initialize nested outputs
        outputs: DetectionResult = {"cues": {}, "combined": {}}
        norm_maps: Dict[str, np.ndarray] = {}

        # Per-method cue blocks
        for method in self.methods:
            edge_map = self._run_extractor(method, image_data)
            block: CueBlock = {"map": edge_map}

            if self.return_density:
                density = compute_edge_density(edge_map, window_size=self.density_window_size)
                block["density"] = density

            if self.return_salience:
                strength = edge_map.astype(np.float32)
                density_for_sal = block.get("density", strength)
                sal = compute_edge_salience(
                    edge_strength=strength,
                    edge_density=density_for_sal,
                    strategy=self.salience_strategy
                )
                block["salience"] = sal

            outputs["cues"][method] = block
            norm_maps[method] = edge_map

        # Combined fused outputs
        fused_map = compute_fused_edge_map(
            canny=norm_maps.get("canny"),
            sobel=norm_maps.get("sobel"),
            laplacian=norm_maps.get("laplacian"),
            piotr=norm_maps.get("piotr"),
            strategy=self.intra_fusion_strategy,
            weights=self.intra_fusion_weights
        )
        outputs["combined"]["strength"] = fused_map

        if self.return_density:
            fused_density = compute_edge_density(fused_map, window_size=self.density_window_size)
            outputs["combined"]["density"] = fused_density

        if self.return_salience:
            strength = fused_map.astype(np.float32)
            density_for_sal = outputs["combined"].get("density", strength)
            fused_sal = compute_edge_salience(
                edge_strength=strength,
                edge_density=density_for_sal,
                strategy=self.salience_strategy
            )
            outputs["combined"]["salience"] = fused_sal

        # ─── DEBUG ─── print full nested output for inspection
        print("=== EdgeDetector.detect() STRUCTURE ===")
        print_structure(outputs)
        print("=== End STRUCTURE ===")
        return outputs


    def _run_extractor(self, method: str, image_data: Dict[str, Any]) -> np.ndarray:
        if method == "canny":
            return extract_canny(image_data["rgb"]["padded"], sigma=self.canny_sigma)

        elif method == "sobel":
            return extract_sobel(image_data["gray"]["padded"], ksize=self.sobel_ksize)

        elif method == "laplacian":
            return extract_laplacian(image_data["gray"]["padded"], ksize=self.laplacian_ksize)

        elif method == "piotr":
            return extract_piotr(image_data["rgb"]["padded"], model_path=self.piotr_model_path)
        else:
            raise ValueError(f"Unsupported edge detection method: {method}")