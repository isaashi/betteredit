# src/analyzer/report/report_generator.py

import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
import logging
from typing import Any, Mapping, Optional
from numpy.typing import NDArray


def print_structure(d: Mapping[str, Any], indent: int = 0) -> None:
    prefix = " " * indent
    for k, v in d.items():
        print(f"{prefix}- {k}")
        if isinstance(v, dict):
            print_structure(v, indent + 2)


def clear_outputs_dir(output_dir: str) -> None:
    if not os.path.exists(output_dir):
        return
    for file in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"[WARNING] Failed to delete {file_path}: {e}")


def save_visual_map(
    feature_map: Optional[NDArray[Any]],
    output_path: str,
    *,
    title: str = "",
    cmap: str = "gray",
    save_visuals: bool = True
) -> None:
    """
    Save a single-channel visual map as a PNG image.

    Parameters:
        feature_map (np.ndarray): The 2D array to visualize.
        output_path (str): Full output filepath (e.g. outputs/edge/canny_map.png).
        title (str): Optional figure title.
        cmap (str): Matplotlib colormap to use.
        save_visuals (bool): If False, skip saving and print skipped message.
    """
    if not save_visuals or feature_map is None:
        print(f"[SKIPPED] Skipping visual map for: {output_path}")
        return

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.figure(figsize=(6, 6))
    plt.imshow(feature_map, cmap=cmap)
    if title:
        plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    print(f"[SAVED] Visual map saved to: {output_path}")


def save_histogram(array, output_path, title):
    plt.figure(figsize=(5, 3))
    plt.hist(array.flatten(), bins=100)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def summarize_stats(array: np.ndarray):
    return {
        "min": float(np.min(array)),
        "max": float(np.max(array)),
        "mean": float(np.mean(array)),
        "std": float(np.std(array))
    }


def log_stats(image_name, strategy, stats):
    logging.info(f"[REPORT] {image_name} | strategy: {strategy}")
    logging.info(f"         min:  {stats['min']:.4f}")
    logging.info(f"         max:  {stats['max']:.4f}")
    logging.info(f"         mean: {stats['mean']:.4f}")
    logging.info(f"         std:  {stats['std']:.4f}")