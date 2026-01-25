import numpy as np
from typing import Any, Dict, Optional
from numpy.typing import NDArray
from loguru import logger


def normalize_edge_map(arr: np.ndarray, percentile_clip: float) -> np.ndarray:
    """Normalize edge map based on percentile clipping to handle dense techniques like Sobel."""
    logger.debug("normalize_edge_map called with percentile_clip={}", percentile_clip)
    high = np.percentile(arr, percentile_clip)
    normalized = np.clip(arr / (high + 1e-5), 0, 1)
    logger.debug("Edge map normalized: min={}, max={}", normalized.min(), normalized.max())
    return normalized


def compute_fused_edge_map(
    canny: Optional[NDArray[Any]],
    sobel: Optional[NDArray[Any]],
    laplacian: Optional[NDArray[Any]],
    piotr: Optional[NDArray[Any]],
    strategy: str,
    weights: Optional[Dict[str, float]] = None
) -> NDArray[Any]:
    """
    Computes a fused edge map from multiple cues using the chosen strategy.

    Parameters:
    - canny, sobel, laplacian, piotr: individual edge maps
    - strategy: 'average', 'max', or 'weighted'
    - weights: optional dict for 'weighted'

    Returns:
    - fused edge map (float32), normalized to [0, 1]
    """
    logger.debug("compute_fused_edge_map called with strategy={}, weights={}", strategy, weights)

    # Ensure weights dict exists for .get()
    wts: Dict[str, float] = weights or {}

    # Gather provided maps
    maps: Dict[str, NDArray[Any]] = {}
    for name, arr in [("canny", canny), ("sobel", sobel), ("laplacian", laplacian), ("piotr", piotr)]:
        if arr is not None:
            maps[name] = arr.astype(np.float32)

    if not maps:
        logger.error("No edge maps provided for intra-fusion.")
        raise ValueError("No edge maps provided for intra-fusion.")

    # Normalize each map (use 99th percentile by default)
    norm_maps: Dict[str, NDArray[Any]] = {
        name: normalize_edge_map(arr, percentile_clip=wts.get("percentile_clip", 99))
        for name, arr in maps.items()
    }

    # Fuse maps
    if strategy == "average":
        fused = sum(norm_maps.values()) / len(norm_maps)
    elif strategy == "max":
        fused = np.maximum.reduce(list(norm_maps.values()))
    elif strategy == "weighted":
        # Default weights if none provided
        default_wts: Dict[str, float] = {"piotr": 0.4, "canny": 0.3, "sobel": 0.15, "laplacian": 0.15}
        active_wts = {**default_wts, **wts}
        cues: list[NDArray[Any]] = []
        total_weight = 0.0
        for name, norm in norm_maps.items():
            weight = active_wts.get(name, 0.0)
            cues.append(weight * norm)
            total_weight += weight
        if total_weight <= 0.0:
            logger.error("All intra-fusion weights are zero.")
            raise ValueError("All intra-fusion weights are zero.")
        fused = sum(cues) / total_weight
    else:
        logger.error("Unsupported intra-fusion strategy: {}", strategy)
        raise ValueError(f"Unsupported intra-fusion strategy: {strategy}")

    # Final normalization
    fused_arr = np.asarray(fused)
    mn, mx = fused_arr.min(), fused_arr.max()
    normed = (fused_arr - mn) / (mx - mn + 1e-8)
    fused_norm = normed.astype(np.float32)
    logger.debug("Fused edge map computed: shape={}, dtype={}", fused_norm.shape, fused_norm.dtype)
    return fused_norm

