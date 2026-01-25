import numpy as np
from typing import Any, Dict, Optional
from numpy.typing import NDArray
from loguru import logger


def compute_cue_salience(
    strength: NDArray[Any],
    density: NDArray[Any],
    strategy: str,
    eps: float = 1e-3
) -> NDArray[Any]:
    """
    Compute salience for a single cue given its strength and local density.

    Strategies:
    - product:    sal = (strength + eps) * (1 - density + eps)
    - ratio:      sal = strength / (density + eps)
    - difference: sal = strength - density
    """
    logger.debug("compute_cue_salience called with strategy={}, eps={}", strategy, eps)
    s = strength.astype(np.float32)
    d = density.astype(np.float32)
    if strategy == "product":
        sal = (s + eps) * (1 - d + eps)
    elif strategy == "ratio":
        sal = s / (d + eps)
    elif strategy == "difference":
        sal = s - d
    else:
        logger.error("Unknown cue salience strategy: {}", strategy)
        raise ValueError(f"Unknown cue salience strategy: {strategy}")

    # ensure array
    sal_arr: NDArray[Any] = np.asarray(sal, dtype=np.float32)
    mn = float(sal_arr.min())
    mx = float(sal_arr.max())
    sal_norm: NDArray[Any] = ((sal_arr - mn) / (mx - mn + eps)).astype(np.float32)
    logger.debug("Cue salience computed: min={:.4f}, max={:.4f}", sal_norm.min(), sal_norm.max())
    return sal_norm


def compute_salience(
    hue_contrast: NDArray[Any],
    saturation: NDArray[Any],
    rarity: Optional[NDArray[Any]],
    luminance_contrast: Optional[NDArray[Any]],
    strategy: str,
    weights: Optional[Dict[str, float]],
    eps: float = 1e-3
) -> NDArray[Any]:
    """
    Computes color-based visual salience using configurable strategy.
    strategy: 'minimal', 'boosted', 'full', 'sum', or 'weighted'
    """
    logger.debug("compute_salience called with strategy={}, weights={}", strategy, weights)

    # safe weights dict
    wts: Dict[str, float] = weights or {}
    # declare salience variable type
    salience: NDArray[Any]

    if strategy == "minimal":
        salience = (hue_contrast + eps) * (saturation + eps)

    elif strategy == "boosted":
        salience = (hue_contrast + eps) * (saturation + eps)
        if rarity is not None:
            salience *= (1 + rarity)

    elif strategy == "full":
        salience = (hue_contrast + eps) * (saturation + eps)
        if rarity is not None:
            salience *= (1 + rarity)
        if luminance_contrast is not None:
            salience *= (1 + luminance_contrast)

    elif strategy == "sum":
        parts = [hue_contrast, saturation]
        if rarity is not None:
            parts.append(rarity)
        if luminance_contrast is not None:
            parts.append(luminance_contrast)
        salience = np.mean(np.stack(parts, axis=0), axis=0)

    elif strategy == "weighted":
        weighted_maps: list[NDArray[Any]] = []
        total_w = 0.0
        for key, arr in [("hue", hue_contrast), ("sat", saturation), ("rarity", rarity), ("lum", luminance_contrast)]:
            if arr is not None:
                w = wts.get(key, 0.0)
                weighted_maps.append(w * arr)
                total_w += w
        if total_w <= 0.0:
            logger.error("All intra-fusion weights are zero.")
            raise ValueError("All intra-fusion weights are zero.")
        # use numpy to sum arrays and ensure ndarray type
        stacked = np.stack(weighted_maps, axis=0)
        salience = np.sum(stacked, axis=0) / total_w
    else:
        logger.error("Unknown salience intra-fusion strategy: {}", strategy)
        raise ValueError(f"Unknown salience intra-fusion strategy: {strategy}")

    # ensure ndarray output
    sal_arr: NDArray[Any] = np.asarray(salience, dtype=np.float32)
    mn = float(sal_arr.min())
    mx = float(sal_arr.max())
    sal_norm: NDArray[Any] = ((sal_arr - mn) / (mx - mn + eps)).astype(np.float32)
    logger.debug("Color salience computed: min={:.4f}, max={:.4f}", sal_norm.min(), sal_norm.max())
    return sal_norm

