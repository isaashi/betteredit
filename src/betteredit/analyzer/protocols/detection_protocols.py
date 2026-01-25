from typing import Dict, TypedDict, Optional
import numpy as np


class CueBlock(TypedDict, total=False):
    """
    Per-cue (or per-method) output block.
    """
    # raw response for this cue
    map: np.ndarray
    # local concentration of the cue response
    density: np.ndarray
    # context-aware "stand-out" score for this cue
    salience: np.ndarray


class CombinedBlock(TypedDict, total=False):
    """
    Fused output across all cues.
    """
    # fused strength map (e.g. weighted sum of cue maps)
    strength: np.ndarray
    # local concentration of fused strength
    density: np.ndarray
    # salience of the fused strength map
    salience: np.ndarray


class DetectionResult(TypedDict, total=False):
    """
    Unified detection output schema.

    - `cues`: per-cue outputs (map, density, salience)
    - `combined`: fused outputs (strength, density, salience)
    - other optional sections (e.g. for object detection placeholders)
    """
    cues: Dict[str, CueBlock]
    combined: CombinedBlock
    # placeholder for object detection boxes or features
    detections: Optional[np.ndarray]
    # placeholder for semantic segmentation
    segmentation: Optional[np.ndarray]