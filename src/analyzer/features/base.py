import logging
import numpy as np
from typing import Any, Dict, List, Tuple

from src.analyzer.features.edge_detection.base import EdgeDetector
from src.analyzer.features.color_detection.base import ColorDetector

from src.betteredit.analyzer.protocols.edge_detector_protocol import EdgeDetectorProtocol
from src.betteredit.analyzer.protocols.color_detector_protocol import ColorDetectorProtocol
from src.betteredit.analyzer.protocols.object_detector_protocol import ObjectDetectorProtocol
from src.betteredit.analyzer.protocols.inter_fusion_strategy_protocol import InterFusionStrategyProtocol
from src.betteredit.analyzer.protocols.human_saliency_model_protocol import HumanSaliencyModelProtocol
from src.betteredit.config import EdgeDetectionConfig, ColorDetectionConfig, Settings


class FeatureExtractor:
    def __init__(
        self,
        enable_color: bool,
        enable_edges: bool,
        enable_objects: bool,
        enable_saliency: bool,
        use_dl_models: bool,
        color_detector_config: ColorDetectionConfig,
        edge_detector_config:   EdgeDetectionConfig
    ):
        self.enable_color = enable_color
        self.enable_edges = enable_edges
        self.enable_objects = enable_objects
        self.enable_saliency = enable_saliency
        self.use_dl_models = use_dl_models
        self.color_detector_config = color_detector_config
        self.edge_detector_config = edge_detector_config

        self.engines: List[Tuple[str, Any]] = []

        self._load_models()


    def _load_models(self):
        if self.enable_edges:
            edge_engine: EdgeDetectorProtocol = EdgeDetector(self.edge_detector_config)
            self.engines.append(("edges", edge_engine))

        if self.enable_color:
            color_engine: ColorDetectorProtocol = ColorDetector(self.color_detector_config)
            self.engines.append(("color", color_engine))

        if self.enable_objects:
            # object_engine: ObjectDetectorProtocol = self._load_object_detector()
            # self.engines.append(("objects", object_engine))
            pass

        if self.enable_saliency and self.use_dl_models:
            # saliency_engine: HumanSaliencyModelProtocol = self._load_saliency_model()
            # self.engines.append(("saliency", saliency_engine))
            pass


    def extract(self, image_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dispatch image_data to each enabled engine via its Protocol.
        Returns a dict: { "edges": {...}, "color": {...}, ... }.

        - If a detector returns {"cues":…, "combined":…}, we flatten those two
          into one level so legacy callers still work.
        - We also always inject `detections` and `segmentation` keys (None by default)
          so future object/segmentation modules slot in cleanly.
        """
        logging.info("[EXTRACT] Starting feature extraction via interfaces...")
        features: Dict[str, Any] = {}
        for name, engine in self.engines:
            raw = engine.detect(image_data)

            # flatten the new schema for backwards compatibility
            if isinstance(raw, dict) and "cues" in raw and "combined" in raw:
                merged = {**raw["cues"], **raw["combined"]}
            else:
                merged = raw

            # always add placeholders for detections/segmentation
            if isinstance(merged, dict):
                merged.setdefault("detections", None)
                merged.setdefault("segmentation", None)

            features[name] = merged

        logging.info("[EXTRACT] Feature extraction complete.")

        return features