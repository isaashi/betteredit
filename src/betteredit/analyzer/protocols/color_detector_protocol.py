from typing import Any, Dict, Protocol
from .detection_protocols import DetectionResult

class ColorDetectorProtocol(Protocol):
    def detect(self, image_data: Dict[str, Any]) -> DetectionResult: ...