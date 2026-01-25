# src/analyzer/inter_fusion/strategies.py

"""
Classical Inter-Fusion Strategies

This module implements Classical Inter-Fusion: rule-based fusion across all final components
(Color, Edge, Objects, Saliency, etc.) to produce final outputs (Visual Weight Heatmap, Eye Flow Path, etc.).

Note: These classes implement InterFusionStrategyProtocol but are not currently used in the pipeline.
"""

from typing import Any, Dict
from numpy.typing import NDArray
from src.betteredit.analyzer.protocols.inter_fusion_strategy_protocol import InterFusionStrategyProtocol

class WeightedFusion(InterFusionStrategyProtocol):
    """
    Final, cross-domain fusion of per-module salience maps (edge, color, object…).
    
    Classical Inter-Fusion: Weighted sum of normalized component maps.
    Fuses final components (Color, Edge, Objects, Saliency, etc.) using configurable weights
    to produce final outputs (Visual Weight Heatmap, Eye Flow Path, etc.).
    """
    def __init__(self, weights: Dict[str, float]):
        self.weights = weights

    def fuse(self, maps: Dict[str, NDArray[Any]]) -> NDArray[Any]:
        # 1) normalize each domain map into [0,1]
        normed: Dict[str, NDArray[Any]] = {}
        for key, arr in maps.items():
            mn, mx = arr.min(), arr.max()
            normed[key] = (arr - mn) / (mx - mn + 1e-8)

        # 2) weighted sum
        total: NDArray[Any] = None  # type: ignore[assignment]
        for key, arr in normed.items():
            w = self.weights.get(key, 1.0)
            term = w * arr
            total = term if total is None else total + term

        # 3) final normalization
        mn, mx = total.min(), total.max()
        result: NDArray[Any] = (total - mn) / (mx - mn + 1e-8)
        return result


class SumFusion(InterFusionStrategyProtocol):
    """
    Simple cross-domain fusion by unweighted sum.
    
    Classical Inter-Fusion: Unweighted sum of normalized component maps.
    Fuses final components (Color, Edge, Objects, Saliency, etc.) using equal weights
    to produce final outputs (Visual Weight Heatmap, Eye Flow Path, etc.).
    """
    def fuse(self, maps: Dict[str, NDArray[Any]]) -> NDArray[Any]:
        total: NDArray[Any] = None  # type: ignore[assignment]
        for arr in maps.values():
            total = arr if total is None else total + arr
        mn, mx = total.min(), total.max()
        result: NDArray[Any] = (total - mn) / (mx - mn + 1e-8)
        return result

