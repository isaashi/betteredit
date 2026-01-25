from typing import Any, Protocol
from numpy.typing import NDArray
from .detection_protocols import DetectionResult

class ObjectDetectorProtocol(Protocol):
    def detect(self, image_rgb: NDArray[Any]) -> DetectionResult: ...