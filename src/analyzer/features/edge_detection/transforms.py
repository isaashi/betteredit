import numpy as np
from scipy.ndimage import uniform_filter  # type: ignore[import-untyped]
from typing import Any
from numpy.typing import NDArray
from loguru import logger


def normalize(arr: NDArray[Any]) -> NDArray[Any]:
    """Normalize an array to [0,1] range."""
    min_val = arr.min()
    max_val = arr.max()
    logger.debug("Normalizing array: min={}, max={}", min_val, max_val)
    return (arr - min_val) / (max_val - min_val + 1e-8)


def compute_edge_density(edge_map: NDArray[Any], window_size: int) -> NDArray[Any]:
    """
    Computes edge density over local regions.
    Inputs:
        - edge_map: binary or probabilistic edge map (0–255 or 0–1)
        - window_size: size of the square window for local density (from config)
    Returns:
        - density map (float32, normalized [0, 1])
    """
    logger.debug("compute_edge_density called with window_size={}", window_size)
    # Ensure float representation
    if edge_map.dtype != np.float32:
        edge_map = edge_map.astype(np.float32)

    binary_map = (edge_map > 0).astype(np.float32)
    density = uniform_filter(binary_map, size=window_size)
    density_norm = normalize(density)
    logger.debug("Edge density computed: shape={}, dtype={}", density_norm.shape, density_norm.dtype)
    return density_norm


def compute_edge_salience(
    edge_strength: NDArray[Any],
    edge_density: NDArray[Any],
    strategy: str
) -> NDArray[Any]:
    """
    Combines edge strength and density into a salience map.
    strategy:
        - "product": salience = (strength+eps) × (density+eps)
        - "sum":     salience = (strength + density) / 2
    """
    logger.debug("compute_edge_salience called with strategy={}", strategy)
    s = normalize(edge_strength)
    d = normalize(edge_density)

    if strategy == "product":
        salience = (s + 1e-3) * (d + 1e-3)
    elif strategy == "sum":
        salience = (s + d) / 2.0
    else:
        logger.error("Unsupported edge salience strategy: {}", strategy)
        raise ValueError(f"Unsupported edge salience intra-fusion strategy: {strategy}")

    sal_norm = normalize(salience)
    logger.debug("Edge salience computed: shape={}, dtype={}", sal_norm.shape, sal_norm.dtype)
    return sal_norm