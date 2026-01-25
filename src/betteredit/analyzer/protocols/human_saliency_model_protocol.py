from typing import Any, Protocol
from numpy.typing import NDArray
from .detection_protocols import DetectionResult

class HumanSaliencyModelProtocol(Protocol):
    def predict(self, image_rgb: NDArray[Any]) -> DetectionResult: ...