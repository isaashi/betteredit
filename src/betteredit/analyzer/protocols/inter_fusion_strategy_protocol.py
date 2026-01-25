from typing import Any, Dict, Protocol
from numpy.typing import NDArray

class InterFusionStrategyProtocol(Protocol):
    def fuse(self, maps: Dict[str, NDArray[Any]]) -> NDArray[Any]: ...

