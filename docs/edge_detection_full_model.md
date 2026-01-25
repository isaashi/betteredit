# Edge Detection Engine Framework

---

## Core Philosophy

| Tier               | Role                                                 | Examples                                   |
|--------------------|------------------------------------------------------|--------------------------------------------|
| Primary Concepts   | Direct edge maps from detection algorithms           | Canny, Piotr, Sobel                        |
| Derived Concepts   | Local transformations over edge maps                 | Edge density, sharpness, orientation       |
| Composite Concepts | Structural inference using spatial/statistical cues | Edge salience, anchoring, flow continuity  |

---

## Phase 1: Primary Concepts

| Concept         | Extracted From        | Description                            |
|------------------|------------------------|----------------------------------------|
| Canny Map        | Grayscale image        | Binary edges using intensity thresholds     |
| Piotr Edge Map   | RGB image              | Probabilistic structured edge strength |
| Sobel Gradient   | Grayscale or luminance | Directional gradients (X, Y)           |
| Laplacian        | Grayscale              | Second-order zero-crossings            |

---

## Phase 2: Derived Concepts

| Concept               | Derived From            | Description                                     |
|------------------------|-------------------------|-------------------------------------------------|
| Edge Density           | Binary edge map         | Percentage of edge pixels per patch             |
| Edge Sharpness         | Gradient magnitude map  | Strength of edge transitions                    |
| Local Edge Variance    | Edge magnitude maps     | Texture/complexity based on std dev             |
| Edge Orientation       | Sobel X/Y               | Local dominant gradient direction (angle)       |

---

## Phase 3: Composite Concepts

| Concept                   | Built From                         | Description                                     |
|----------------------------|------------------------------------|-------------------------------------------------|
| Edge Salience             | Edge strength × density            | Emphasis on detailed and strong structures      |
| Contour Coherence         | Connected components + orientation | Continuous edge groupings                       |
| Structural Anchors        | Edge maps + layout grid            | Are edges aligned to expected composition zones |

---

## Phase 4: Statistical and Spatial Concepts

| Concept                    | Derived From              | Description                                 |
|----------------------------|---------------------------|---------------------------------------------|
| Edge Coverage              | Binary edge maps          | Percentage of total pixels that are edges   |
| Orientation Histogram      | Quantized edge directions | Distribution of gradient directions         |
| Edge Distribution Balance  | Edge density by grid      | Positional symmetry in edge presence        |

---

## Phase 5: Physical Cues and Composition-Aware Modeling

| Concept              | Derived From         | Description                                  |
|----------------------|----------------------|----------------------------------------------|
| Luminance Edges      | Grayscale gradient   | Brightness-based edge transitions            |
| Chromatic Edges      | HSV / LAB            | Color-based edge transitions                 |
| Combined Gradients   | Luminance + chroma   | Unified perceptual edge measure              |

| Concept               | Derived From / Built On         | Description                              |
|------------------------|---------------------------------|------------------------------------------|
| Flow Linearity         | Gradient field + direction map  | Coherent directional movement            |
| Symmetry Anchors       | Edge maps across axes           | Positional mirroring in edge patterns    |

---

## Roadmap by Tiered Phase

| Tier / Phase                     | Scope                                      |
|----------------------------------|--------------------------------------------|
| Phase 1: Primary Concepts        | Extract raw edge maps from core algorithms |
| Phase 2: Derived Concepts        | Quantify edges: density, strength, direction |
| Phase 3: Composite Concepts      | Build higher-order reasoning over edges    |
| Phase 4: Statistical & Spatial   | Analyze edge coverage, directionality, bias |
| Phase 5: Physical + Composition  | Integrate edges with layout and perception  |