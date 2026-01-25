# betteredit: Architecture Understanding

This document captures the shared understanding of the betteredit architecture to ensure consistency in design decisions.

---

## Core Architecture Principles

### 1. Multiple Image-Defining Components

An image is defined by multiple components, not just Color and Edge:
- **Color**: RGB, HSV, LAB, contrast, clusters, harmony
- **Edge**: Canny, Sobel, gradients, structure, flow
- **Objects**: Object detection, semantic segmentation (planned)
- **Saliency**: Human attention models (planned)
- **Texture**: Patterns, granularity (potential)
- **Depth**: 3D structure, distance (potential)
- **Motion**: Movement, flow (potential)

**Current Implementation**: Color and Edge are implemented. Objects and Saliency are planned (flags exist in `FeatureExtractor`).

---

### 2. Abstraction Levels Within Each Component

Each component has multiple abstraction levels, from low-level (fundamental) to high-level (semantic):

#### Color Component Example:
- **Phase 1 (Primary)**: RGB, HSV, LAB → **Classical** (mathematical color space conversions)
- **Phase 2 (Derived)**: Hue Contrast, Luminance Contrast → **Classical** (mathematical transformations)
- **Phase 3 (Composite)**: Salience, Rarity, Harmony → **Mix** (some classical, some neural)
- **Phase 4 (Statistical)**: Color Clusters (KMeans/VAE) → **Neural** (learned patterns)
- **Phase 5 (Integration)**: Contextual Importance (Color + Objects/Edges) → **Neural** (semantic understanding)

#### Edge Component Example:
- **Phase 1 (Primary)**: Canny, Sobel, Laplacian → **Classical** (mathematical edge detection)
- **Phase 2 (Derived)**: Edge Density, Sharpness → **Classical** (mathematical transformations)
- **Phase 3 (Composite)**: Edge Salience, Contour Coherence → **Mix**
- **Phase 4 (Statistical)**: Edge Coverage, Orientation Histogram → **Mix/Neural**
- **Phase 5 (Integration)**: Flow Linearity, Semantic Edge Understanding → **Neural**

**Key Principle**: Low-level features (RGB, HSV, basic edges) are classical. High-level features (clusters, semantic understanding, contextual importance) require neural techniques.

---

### 3. Two-Level Fusion Architecture

#### Level 1: **Intra-Fusion** (Within Each Component)

**Definition**: Fusion of classical + neural sub-components within a single component to produce the final component representation.

**Types**:
- **Classical Intra-Fusion**: Rule-based fusion (weighted sum, product, max) of classical + neural sub-components within a component
- **Neural Intra-Fusion**: Learned fusion of classical + neural sub-components within a component (future enhancement)

**Example - Color Component**:
```
Classical Sub-components:
  - RGB, HSV, LAB (Phase 1)
  - Hue Contrast, Luminance Contrast (Phase 2)
  - Some Composite concepts (Phase 3)

Neural Sub-components:
  - Color Clusters (KMeans/VAE) (Phase 4)
  - Contextual Importance (Phase 5)

Final Color Component (optimal mix of classical + neural)
```

**Example - Edge Component**:
```
Classical Sub-components:
  - Canny, Sobel, Laplacian (Phase 1)
  - Edge Density, Sharpness (Phase 2)

Neural Sub-components:
  - Semantic Edge Understanding (Phase 5)
  - Flow Linearity (Phase 5)

Final Edge Component (optimal mix of classical + neural)
```

---

#### Level 2: **Inter-Fusion** (Across All Components)

**Definition**: Fusion of all final components (Color, Edge, Objects, Saliency, etc.) to produce final outputs (Visual Weight Heatmap, Eye Flow Path, etc.).

**Types**:
- **Classical Inter-Fusion**: Rule-based fusion (weighted sum) of all final components (`WeightedFusion`, `SumFusion` in `inter_fusion/strategies.py`)
- **Neural Inter-Fusion**: Learned fusion of all final components

**Important Note**: The current design is to **SELECT** either classical OR neural inter-fusion via configuration (`inter_fusion_strategy: "classical" | "neural"`), not combine both. The factory/selector pattern chooses one strategy. Combining both outputs (e.g., ensemble approach) could be a future enhancement, but it's not in the current implementation plan.

**Example**:
```
Final Color Component
Final Edge Component
Final Object Component
Final Saliency Component
... (other components)

↓ Inter-Fusion (Classical or Neural, configurable - SELECT one) ↓

Final Outputs:
  - Visual Weight Heatmap
  - Eye Flow Path Overlay
  - Salience Map
  - Visual Hierarchy Analysis
  - ... (other outputs)
```

---

### 4. Complete Architecture Flow

```
Input Image
    ↓
[Component Extraction - Each with Classical + Neural sub-components]
    ├─ Color Component
    │   ├─ Classical: RGB, HSV, LAB, Hue Contrast, Luminance Contrast
    │   ├─ Neural: Color Clusters (KMeans/VAE), Contextual Importance
    │   └─ → Classical Intra-Fusion → Final Color Component
    │
    ├─ Edge Component
    │   ├─ Classical: Canny, Sobel, Laplacian, Edge Density
    │   ├─ Neural: Semantic Edge Understanding, Flow Linearity
    │   └─ → Classical Intra-Fusion → Final Edge Component
    │
    ├─ Object Component (planned)
    │   ├─ Classical: (basic shape detection?)
    │   ├─ Neural: Object Detection, Semantic Segmentation
    │   └─ → Classical Intra-Fusion → Final Object Component
    │
    └─ Saliency Component (planned)
        ├─ Classical: (basic attention heuristics?)
        ├─ Neural: Human Saliency Models (DeepGaze, SalGAN)
        └─ → Classical Intra-Fusion → Final Saliency Component
    ↓
[Inter-Fusion - Classical or Neural (configurable, SELECT one) across all components]
    └─ → Fused Multi-Component Representation
    ↓
[Final Output Generation]
    ├─ Visual Weight Heatmap = Inter-Fusion(Color, Edge, Objects, Saliency, ...)
    ├─ Eye Flow Path = Inter-Fusion(Color, Edge, Objects, ...)
    ├─ Salience Map = Inter-Fusion(Color, Edge, Objects, Saliency, ...)
    ├─ Visual Hierarchy = Inter-Fusion(Color, Edge, Objects, ...)
    └─ ... (other outputs)

```

---

### 5. Key Design Principles

#### A. Each final output (Visual Weight Heatmap, etc.) is a **single fused result** that leverages both classical and neural strengths

#### B. Classical for Low-Level, Neural for High-Level
- **Classical**: Mathematical operations, color space conversions, basic edge detection (fast, interpretable, well-understood)
- **Neural**: Semantic understanding, learned patterns, contextual importance (requires learning, captures complex relationships)
- **Boundary**: The boundary between classical and neural depends on the abstraction level and complexity of the task

#### C. Component Independence
- Each component (Color, Edge, Objects, etc.) can be developed independently
- Components follow the same pattern: classical + neural sub-components → intra-fusion → final component
- Components are then combined via inter-fusion

---

### 6. Terminology

- **Classical Intra-Fusion**: Rule-based fusion (weighted sum, product, max) within a single component
- **Neural Intra-Fusion**: Learned fusion within a single component
- **Classical Inter-Fusion**: Rule-based fusion (weighted sum) across all components
- **Neural Inter-Fusion**: Learned fusion across all components
- **Component**: A major image-defining aspect (Color, Edge, Objects, Saliency, etc.)
- **Sub-component**: A specific feature within a component (e.g., RGB is a sub-component of Color)
- **Final Output**: The end result (Visual Weight Heatmap, Eye Flow Path, etc.)

---

### 7. Current State vs. Target State

#### Current Implementation:
- [IMPLEMENTED] Color Component: Classical sub-components implemented, neural sub-components partially implemented
- [IMPLEMENTED] Edge Component: Classical sub-components implemented, neural sub-components partially implemented
- [PLANNED] Object Component: Planned (protocols exist, not implemented)
- [PLANNED] Saliency Component: Planned (protocols exist, not implemented)
- [IMPLEMENTED] Classical Intra-Fusion: Implemented (functions in `color_detection/intra_fusion.py` and `edge_detection/intra_fusion.py`)
- [PLANNED] Neural Intra-Fusion: Future enhancement
- [PLANNED] Classical Inter-Fusion: Implemented but not integrated in pipeline (`WeightedFusion`, `SumFusion` in `inter_fusion/strategies.py`)
- [IN PROGRESS] Neural Inter-Fusion: In progress

#### Target State:
- All components fully implemented with both classical and neural sub-components
- Intra-fusion for each component (optimal classical + neural combination)
- Inter-fusion across all components (classical/ neural fusion)
- Multiple final outputs generated from inter-fused components

---

### 8. References

- `docs/color_detection_full_model.md`: Color component phases and abstraction levels
- `docs/edge_detection_full_model.md`: Edge component phases and abstraction levels
- `docs/inter_fusion_full_model.md`: Final outputs and their requirements
- `src/analyzer/features/base.py`: Component extraction architecture
- `src/analyzer/inter_fusion/strategies.py`: Classical Inter-Fusion strategies (`WeightedFusion`, `SumFusion`)