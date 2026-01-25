import cv2
import numpy as np
from typing import Any, Optional
from numpy.typing import NDArray
import os
import urllib.request
from loguru import logger


def extract_canny(image_rgb: NDArray[Any], sigma: float = 0.33) -> NDArray[Any]:
    """Canny edge detection with automatic thresholding using median-based heuristics."""
    logger.debug("extract_canny called with sigma={}", sigma)
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    v: float = float(np.median(gray))
    lower: int = int(max(0.0, (1.0 - sigma) * v))
    upper: int = int(min(255.0, (1.0 + sigma) * v))
    edges = cv2.Canny(gray, lower, upper)
    logger.debug("Canny edges computed: shape={}, dtype={}", edges.shape, edges.dtype)
    return edges


def extract_sobel(gray_img: NDArray[Any], ksize: int = 3) -> NDArray[Any]:
    """Compute gradient magnitude using Sobel filters."""
    logger.debug("extract_sobel called with ksize={}", ksize)
    gx = cv2.Sobel(gray_img, cv2.CV_32F, 1, 0, ksize=ksize)
    gy = cv2.Sobel(gray_img, cv2.CV_32F, 0, 1, ksize=ksize)
    grad = np.sqrt(gx**2 + gy**2)
    sobel = cv2.normalize(grad, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)  # type: ignore[call-overload]
    logger.debug("Sobel edges computed: shape={}, dtype={}", sobel.shape, sobel.dtype)
    return sobel


def extract_laplacian(
    gray_img: NDArray[Any],
    ksize: int = 3,
    blur_size: int = 3,
    blur_sigma: float = 1.0
) -> NDArray[Any]:
    """
    Smoothed Laplacian edge detection (Laplacian of Gaussian).
    Applies Gaussian blur before computing the second derivative.
    """
    logger.debug(
        "extract_laplacian called with ksize={}, blur_size={}, blur_sigma={}",
        ksize, blur_size, blur_sigma
    )
    blurred = cv2.GaussianBlur(gray_img, (blur_size, blur_size), sigmaX=blur_sigma)
    lap = cv2.Laplacian(blurred, cv2.CV_32F, ksize=ksize)
    abs_lap = np.abs(lap)
    lap_norm = cv2.normalize(abs_lap, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)  # type: ignore[call-overload]
    logger.debug("Laplacian edges computed: shape={}, dtype={}", lap_norm.shape, lap_norm.dtype)
    return lap_norm


def extract_piotr(image_rgb: NDArray[Any], model_path: str = "models/model.yml.gz") -> NDArray[Any]:
    """Piotr Dollar's Structured Edge Detection using OpenCV ximgproc bindings."""
    logger.debug("extract_piotr called with model_path='{}'", model_path)
    try:
        from cv2 import ximgproc
    except ImportError:
        logger.error("cv2.ximgproc module not available.")
        raise ImportError("cv2.ximgproc module not available. Ensure opencv-contrib-python is installed.")

    if not os.path.exists(model_path):
        logger.info("Piotr model not found at '{}'. Downloading...", model_path)
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        url = "https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/cv/ximgproc/model.yml.gz"
        urllib.request.urlretrieve(url, model_path)
        logger.info("Piotr model downloaded successfully to '{}'.", model_path)

    model = ximgproc.createStructuredEdgeDetection(model_path)

    image_float = image_rgb.astype(np.float32) / 255.0
    edge_map = model.detectEdges(image_float)
    logger.debug("Raw Piotr edge map created: shape={}", edge_map.shape)

    image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
    orientation = model.computeOrientation(image_gray)

    edges_nms = model.edgesNms(edge_map, orientation)
    result = (edges_nms * 255).astype(np.uint8)
    logger.debug("Piotr edges after NMS: shape={}, dtype={}", result.shape, result.dtype)
    return result