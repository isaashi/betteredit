# Protocols Documentation

This document describes all core protocols (interfaces) used across the betteredit project, their method signatures, expected inputs, and return structures. Modules implementing these protocols should adhere exactly to the conventions described below.

## 1. `detection_protocols.py`

Defines common TypedDict schemas for cue-based and fused outputs.

* **`CueBlock`** (per-cue):

  * `map` (required if that cue exists): 2D `np.ndarray` (H×W) of raw feature values.
  * `density` (optional): 2D `np.ndarray` representing local concentration of responses.
  * `salience` (optional): 2D `np.ndarray` representing context-aware "stand-out" scores.

* **`CombinedBlock`** (fused):

  * `strength` (required if fused map exists): 2D `np.ndarray` (H×W) of combined feature strength.
  * `density` (optional): 2D `np.ndarray` of local concentration for the fused map.
  * `salience` (optional): 2D `np.ndarray` of salience for the fused map.
  
  **Note**: This represents **Classical Intra-Fusion** (fusion within a component, e.g., combining all color cues into a final color component).

* **`DetectionResult`** (overall schema):

  * `cues` (Dict\[str, CueBlock]): Maps cue names (e.g., "canny", "hue") to their respective `CueBlock`.
  * `combined` (CombinedBlock): The fused output (strength, optional density/salience). This is the result of **Classical Intra-Fusion** within the component.
  * `detections` (optional `np.ndarray`): For object detectors, an array of bounding boxes or detection values.
  * `segmentation` (optional `np.ndarray`): For segmentation modules, a mask array of shape H×W.

All modules returning any cue-based or fused output should return a `DetectionResult` conforming to this schema.

**Fusion Terminology**:
- **Classical Intra-Fusion**: Rule-based fusion within a component (combining all cues/sub-components of that component). The `combined` field in `DetectionResult` represents Classical Intra-Fusion. Currently implemented as functions in `color_detection/intra_fusion.py` and `edge_detection/intra_fusion.py`.
- **Neural Intra-Fusion**: Learned fusion within a component (future enhancement).
- **Classical Inter-Fusion**: Rule-based fusion across all components (combining Color, Edge, Objects, Saliency, etc. to produce final outputs). `WeightedFusion` and `SumFusion` in `inter_fusion/strategies.py` implement this but are not currently used in the pipeline.
- **Neural Inter-Fusion**: Learned fusion across all components.

**Important Note**: The current design is to **SELECT** either classical OR neural inter-fusion via configuration (`inter_fusion_strategy: "classical" | "neural"`), not combine both. The factory/selector pattern chooses one strategy. Combining both outputs (e.g., ensemble approach) could be a future enhancement, but it's not in the current implementation plan.

---

## 2. `ColorDetectorProtocol` (in `color_detection_protocol.py`)

* **Method**: `detect(image_data) -> DetectionResult`

* **`image_data` keys**:

  * `"image"`: `np.ndarray` of shape (H×W×3), RGB image.
  * `"metadata"`: `Dict[str, Any]`, EXIF or camera parameters.
  * (Optional) any precomputed buffers (e.g., resized image under a different key).

* **Return**: A `DetectionResult` with at least:

  * `cues`: For each color cue (e.g., "hue", "saturation", "luminance", "rarity"), provide a `CueBlock` containing:

    * `map`: 2D `np.ndarray` of raw cue values.
    * (Optional) `density` and/or `salience`, based on configuration.
  * `combined`: One `CombinedBlock` containing:

    * `strength`: 2D fused color-strength map.
    * (Optional) `density` and/or `salience`.
  * No need to set `detections` or `segmentation` (leave unset or `None`).

Implementing modules should:

* Read `image_data["image"]` and `image_data["metadata"]`.
* Compute each cue map as a 2D array.
* Populate the per-cue `CueBlock` under `cues[name]`.
* Compute a fused map, store under `combined["strength"]`.
* Optionally compute `density`/`salience` if flags are enabled.

---

## 3. `EdgeDetectorProtocol` (in `edge_detector_protocol.py`)

* **Method**: `detect(image_data) → DetectionResult`

* **`image_data` keys**:

  * `"image"`: `np.ndarray` (H×W×3), RGB image.
  * `"metadata"`: `Dict[str, Any]`.

* **Return**: A `DetectionResult` with:

  * `cues`: Each edge method name (e.g., "canny", "sobel", "laplacian", "piotr") maps to a `CueBlock`:

    * `map`: 2D edge-strength array.
    * (Optional) `density` and/or `salience`, based on flags.
  * `combined`: A `CombinedBlock` with:

    * `strength`: 2D fused edge-strength map.
    * (Optional) `density`, `salience`.
  * `detections`, `segmentation`: Unused (leave unset).

Follow the same pattern as color: read inputs, compute per-method `CueBlock`s, then fuse.

---

## 4. `InterFusionStrategyProtocol` (in `inter_fusion_strategy_protocol.py`)

* **Method**: `fuse(maps) → NDArray[Any]`
* **`maps`**: A dict mapping component names (e.g., "color", "edge", "objects", "saliency") to 2D `np.ndarray` arrays (each normalized to some range, typically \[0,1] or comparable). Each array represents the final fused output from that component (e.g., Final Color Component, Final Edge Component).
* **Return**: A single 2D `np.ndarray` representing the fused map (e.g., weighted sum, product, or max across all input maps).

**Note**: This protocol is designed for **Classical Inter-Fusion** (fusion across all components). For example, combining final Color, Edge, Objects, and Saliency components into final outputs (Visual Weight Heatmap, Eye Flow Path, etc.). The `WeightedFusion` and `SumFusion` classes in `inter_fusion/strategies.py` implement this protocol but are not currently used in the pipeline.

**Note on Intra-Fusion**: Classical Intra-Fusion (within components) is currently implemented as functions in `color_detection/intra_fusion.py` (`compute_salience`) and `edge_detection/intra_fusion.py` (`compute_fused_edge_map`), not via this protocol.

Modules implementing fusion should:

* Accept `maps` where each value is a 2D array of identical shape.
* Output a fused 2D array of that same shape.
* Optionally read fusion weights or strategies from configuration.

---

## 5. `HumanSaliencyModelProtocol` (in `human_saliency_model_protocol.py`)

* **Method**: `predict(image_rgb) → DetectionResult`
* **Input**: `image_rgb` is a 3D `np.ndarray` (H×W×3), RGB image.
* **Return**: A `DetectionResult` with at least:

  * `cues`: A single cue key (e.g., "human\_saliency") mapping to a `CueBlock`:

    * `map`: 2D saliency map (normalized \[0,1]).
    * (Optional) `density` and/or `salience`, if computed.
  * `combined`: Typically identical to the saliency map under `strength`.
  * `detections`, `segmentation`: Unused (leave unset).

Implementing classes should run a DL-based saliency model, produce a 2D saliency heatmap, and package it according to `DetectionResult`.

---

## 6. `ObjectDetectorProtocol` (in `object_detector_protocol.py`)

* **Method**: `detect(image_rgb) → DetectionResult`
* **Input**: A single 3D `np.ndarray` (H×W×3), RGB image.
* **Return**: A `DetectionResult` that may include:

  * `cues`: (Optional) If you want to provide per-object cue maps (e.g., objectness heatmaps). Not required.
  * `combined`: (Optional) A fused mask or combined objectness map.
  * `detections`: A 2D `np.ndarray` of shape (N×4) or (N×5), where each row is `[x1, y1, x2, y2]` or `[x1, y1, x2, y2, score]`.
  * `segmentation`: (Optional) A 2D mask (H×W) with semantic or instance labels.

At minimum, object detectors should populate `detections` with bounding boxes or keypoints. If desired, they can also provide a per-pixel mask under `segmentation`.