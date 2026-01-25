import numpy as np
import cv2
from scipy.ndimage import gaussian_filter, uniform_filter  # type: ignore[import-untyped]
from sklearn.cluster import KMeans
from typing import Any
from numpy.typing import NDArray
from loguru import logger


def normalize(arr: NDArray[Any]) -> NDArray[Any]:
    """Normalize an array to [0,1] range with debug logging."""
    min_val, max_val = arr.min(), arr.max()
    logger.debug("normalize called: min={}, max={}", min_val, max_val)
    return (arr - min_val) / (max_val - min_val + 1e-8)


def compute_hue_contrast(
    hue: NDArray[Any],
    sigma: float
) -> NDArray[Any]:
    """Computes local hue contrast using angular difference with debug logging."""
    logger.debug("compute_hue_contrast called with sigma={}", sigma)
    hue = hue.astype(np.float32)
    hue_sin = np.sin(2 * np.pi * hue)
    hue_cos = np.cos(2 * np.pi * hue)

    mean_sin = gaussian_filter(hue_sin, sigma=sigma)
    mean_cos = gaussian_filter(hue_cos, sigma=sigma)
    mean_angle = np.arctan2(mean_sin, mean_cos) / (2 * np.pi)
    mean_angle %= 1.0

    diff = np.abs(hue - mean_angle)
    contrast = normalize(np.minimum(diff, 1.0 - diff))
    logger.debug("Hue contrast computed: shape={}, dtype={}", contrast.shape, contrast.dtype)
    return contrast


def compute_luminance_contrast(
    luminance: NDArray[Any],
    method: str,
    sobel_weight: float
) -> NDArray[Any]:
    """Computes luminance contrast with debug logging."""
    logger.debug(
        "compute_luminance_contrast called with method={}, sobel_weight={}",
        method, sobel_weight
    )
    
    def sobel_contrast(img: NDArray[Any]) -> NDArray[Any]:
        gx = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=3)
        grad = np.sqrt(gx ** 2 + gy ** 2)
        return normalize(grad)

    def std_contrast(img: NDArray[Any]) -> NDArray[Any]:
        mean = uniform_filter(img, size=5)
        sq_mean = uniform_filter(img ** 2, size=5)
        stddev = np.sqrt(sq_mean - mean ** 2)
        return normalize(stddev)

    if method == "sobel":
        result = sobel_contrast(luminance)
    elif method == "local_std":
        result = std_contrast(luminance)
    elif method == "combined":
        sob = sobel_contrast(luminance)
        std = std_contrast(luminance)
        result = sobel_weight * sob + (1 - sobel_weight) * std
    else:
        logger.error("Unsupported contrast method: {}", method)
        raise ValueError(f"Unsupported contrast method: {method}")

    contrast_norm = normalize(result)
    logger.debug(
        "Luminance contrast computed: shape={}, dtype={}",
        contrast_norm.shape, contrast_norm.dtype
    )
    return contrast_norm


def compute_color_rarity(
    img_bgr: NDArray[Any],
    space: str,
    k: int
) -> NDArray[Any]:
    """Computes global color rarity based on distance from cluster centers with debug logging."""
    logger.debug("compute_color_rarity called with space={}, k={}", space, k)
    h, w = img_bgr.shape[:2]
    if space == "lab":
        img_space = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
        features = img_space[:, :, 1:3].reshape(-1, 2)
    elif space == "hue":
        img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
        hue = img_hsv[:, :, 0].astype(np.float32) / 180.0
        x = np.cos(2 * np.pi * hue)
        y = np.sin(2 * np.pi * hue)
        features = np.stack([x, y], axis=-1).reshape(-1, 2)
    else:
        logger.error("Unsupported color space: {}", space)
        raise ValueError(f"Unsupported color space: {space}")

    kmeans = KMeans(n_clusters=k, n_init='auto')
    labels = kmeans.fit_predict(features)
    centers = kmeans.cluster_centers_
    dists = np.linalg.norm(features - centers[labels], axis=1)
    rarity = dists.reshape(h, w)
    rarity_norm = normalize(rarity)
    logger.debug("Color rarity computed: min={}, max={}", rarity_norm.min(), rarity_norm.max())
    return rarity_norm


def compute_color_density(
    arr: NDArray[Any],
    window_size: int
) -> NDArray[Any]:
    """Computes local variance density with debug logging."""
    logger.debug("compute_color_density called with window_size={}", window_size)
    img = arr.astype(np.float32)
    mean = uniform_filter(img, size=window_size)
    sq_mean = uniform_filter(img ** 2, size=window_size)
    var = sq_mean - mean ** 2
    density_norm = normalize(var)
    logger.debug("Color density computed: shape={}, dtype={}", density_norm.shape, density_norm.dtype)
    return density_norm