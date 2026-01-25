from typing import Any, Dict, Protocol
from .detection_protocols import DetectionResult

class EdgeDetectorProtocol(Protocol):
    def detect(self, image_data: Dict[str, Any]) -> DetectionResult: ...