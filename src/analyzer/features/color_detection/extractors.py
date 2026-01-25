import cv2
import numpy as np
from typing import Any
from numpy.typing import NDArray
from loguru import logger


def extract_hue_map(hsv_img: NDArray[Any]) -> NDArray[Any]:
    """Extract normalized hue channel from HSV image."""
    logger.debug("extract_hue_map called: shape={}, dtype={}", hsv_img.shape, hsv_img.dtype)
    hue = hsv_img[:, :, 0].astype(np.float32) / 180.0
    logger.debug("Hue map computed: min={:.4f}, max={:.4f}", hue.min(), hue.max())
    return hue


def extract_saturation_map(hsv_img: NDArray[Any], sigma: float = 1.0) -> NDArray[Any]:
    """Extract and smooth saturation map."""
    logger.debug("extract_saturation_map called with sigma={}", sigma)
    sat = hsv_img[:, :, 1].astype(np.float32) / 255.0
    blurred = cv2.GaussianBlur(sat, (5, 5), sigmaX=sigma)
    logger.debug(
        "Saturation map computed: shape={}, dtype={}, min={:.4f}, max={:.4f}",
        blurred.shape, blurred.dtype, blurred.min(), blurred.max()
    )
    return blurred


def extract_luminance_map(bgr_img: NDArray[Any]) -> NDArray[Any]:
    """Convert BGR image to LAB and extract luminance (L*)."""
    logger.debug("extract_luminance_map called: shape={}, dtype={}", bgr_img.shape, bgr_img.dtype)
    lab = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2LAB)
    lum = lab[:, :, 0].astype(np.float32) / 255.0
    logger.debug("Luminance map computed: min={:.4f}, max={:.4f}", lum.min(), lum.max())
    return lum