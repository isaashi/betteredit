import cv2
import numpy as np
from PIL import Image, ExifTags
from typing import Dict, Any, Tuple
from src.config.design_registry import DesignRegistry


def normalize_uint8(img: np.ndarray) -> np.ndarray:
    return img.astype(np.float32) / 255.0

def normalize_lab(lab_img: np.ndarray) -> np.ndarray:
    # OpenCV: L ∈ [0,100]; a*/b* ∈ [0,255] with 128 = 0
    l = np.clip(lab_img[:, :, 0], 0, 100) / 100.0
    a = (lab_img[:, :, 1].astype(np.float32) - 128) / 127.0
    b = (lab_img[:, :, 2].astype(np.float32) - 128) / 127.0
    return np.stack([l, a, b], axis=-1).astype(np.float32)

def preprocess_image(
    image_path: str,
    target_size: Tuple[int, int]
) -> Dict[str, Any]:
    # Register preprocessing start
    DesignRegistry.register(
        module="Preprocessing",
        component="Image Processing",
        concept="Preprocessing Start",
        technique="image_loading",
        tuning_params={
            "image_path": image_path,
            "target_size": target_size
        }
    )
    
    image_pil: Image.Image = Image.open(image_path)

    # EXIF extraction
    exif_data = image_pil.getexif()
    exif = {}
    orientation = None
    if exif_data:
        for tag, value in exif_data.items():
            decoded = ExifTags.TAGS.get(tag, tag)
            exif[decoded] = value

        # Orientation correction
        orientation = exif.get("Orientation", None)
        if orientation == 3:
            image_pil = image_pil.rotate(180, expand=True)
        elif orientation == 6:
            image_pil = image_pil.rotate(270, expand=True)
        elif orientation == 8:
            image_pil = image_pil.rotate(90, expand=True)

    # Original aspect
    og_width, og_height = image_pil.size
    original_aspect = og_width / og_height

    # Convert to RGB
    original_rgb = np.array(image_pil.convert("RGB"))
    original_rgb_normalized = normalize_uint8(original_rgb)

    # Resize to target size with padding
    target_w, target_h = target_size
    scale = min(target_w / og_width, target_h / og_height)
    new_w, new_h = int(og_width * scale), int(og_height * scale)
    resized = cv2.resize(original_rgb, (new_w, new_h), interpolation=cv2.INTER_AREA)

    pad_vert = target_h - new_h
    pad_horz = target_w - new_w
    pad_top, pad_bottom = pad_vert // 2, pad_vert - (pad_vert // 2)
    pad_left, pad_right = pad_horz // 2, pad_horz - (pad_horz // 2)

    padded_rgb = cv2.copyMakeBorder(
        resized, pad_top, pad_bottom, pad_left, pad_right,
        borderType=cv2.BORDER_CONSTANT, value=[0, 0, 0]
    )
    padded_rgb_normalized = normalize_uint8(padded_rgb)

    # Generate all image spaces (original and padded)
    def generate_space_views(rgb_img, is_padded=False):
        gray = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2GRAY)
        hsv = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2HSV)
        lab = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2LAB)
        bgr = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2BGR)

        return {
            "rgb": {
                "padded" if is_padded else "og": rgb_img,
                "padded_normalized" if is_padded else "og_normalized": normalize_uint8(rgb_img)
            },
            "bgr": {
                "padded" if is_padded else "og": bgr,
                "padded_normalized" if is_padded else "og_normalized": normalize_uint8(bgr)
            },
            "gray": {
                "padded" if is_padded else "og": gray,
                "padded_normalized" if is_padded else "og_normalized": normalize_uint8(gray)
            },
            "hsv": {
                "padded" if is_padded else "og": hsv,
                "padded_normalized" if is_padded else "og_normalized": normalize_uint8(hsv)
            },
            "lab": {
                "padded" if is_padded else "og": lab,
                "padded_normalized" if is_padded else "og_normalized": normalize_lab(lab)
            }
        }

    original_spaces = generate_space_views(original_rgb, is_padded=False)
    padded_spaces = generate_space_views(padded_rgb, is_padded=True)

    # Merge all modalities by space
    merged = {
        "rgb": {**original_spaces["rgb"], **padded_spaces["rgb"]},
        "bgr": {**original_spaces["bgr"], **padded_spaces["bgr"]},
        "gray": {**original_spaces["gray"], **padded_spaces["gray"]},
        "hsv": {**original_spaces["hsv"], **padded_spaces["hsv"]},
        "lab": {**original_spaces["lab"], **padded_spaces["lab"]},
    }

    result = {
        "exif": exif,
        "original_aspect_ratio": round(original_aspect, 5),
        "padding": {
            "top": pad_top,
            "bottom": pad_bottom,
            "left": pad_left,
            "right": pad_right
        },
        **merged
    }
    
    # Register preprocessing completion with essential info
    DesignRegistry.register(
        module="Preprocessing",
        component="Image Processing",
        concept="Preprocessing Complete",
        technique="image_transformation",
        tuning_params={
            "original_size": [og_width, og_height],
            "target_size": target_size,
            "scale_factor": scale,
            "padding_applied": {
                "top": pad_top,
                "bottom": pad_bottom,
                "left": pad_left,
                "right": pad_right
            },
            "color_spaces_generated": list(merged.keys()),
            "exif_keys": list(exif.keys()) if exif else [],
            "orientation_corrected": orientation is not None and orientation in [3, 6, 8]
        }
    )
    
    return result