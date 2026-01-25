# Color Detection Engine Framework

---

## Core Philosophy

| Tier               | Role                                               | Examples                                   |
|--------------------|----------------------------------------------------|--------------------------------------------|
| Primary Concepts   | Directly extracted from color spaces               | Hue, Saturation, Luminance                 |
| Derived Concepts   | Local transformations or comparisons of primary cues | Hue contrast, luminance contrast         |
| Composite Concepts | Fusion of cues into perceptual or statistical models | Salience, rarity, harmony                |

---

## Phase 1: Primary Concepts

| Concept     | Extracted From | Description                           |
|-------------|----------------|---------------------------------------|
| Hue         | HSV.H          | Angular color type (0–1 normalized)   |
| Saturation  | HSV.S          | Color vividness or purity             |
| Luminance   | LAB.L          | Perceptual brightness (L*)            |
| a*          | LAB.a          | Red–Green axis in LAB space           |
| b*          | LAB.b          | Yellow–Blue axis in LAB space         |
| RGB         | Raw            | Needed for fallback/utility ops       |

---

## Phase 2: Derived Concepts

| Concept               | Derived From        | Description                                |
|------------------------|---------------------|--------------------------------------------|
| Hue Contrast           | Hue                | Local angular deviation                    |
| Luminance Contrast     | Luminance          | Std or Sobel over brightness               |
| Perceptual Color Diff  | LAB or RGB         | ΔE or color distance                       |
| Saturation Gradient    | Saturation         | Local variation, indicates texture         |

---

## Phase 3: Composite Concepts

| Concept                  | Built On                         | Description                                   |
|---------------------------|----------------------------------|-----------------------------------------------|
| Color Rarity              | Clustering on Hue or a*/b*       | Global color uniqueness                       |
| Visual Salience (Color)   | Hue Contrast × Sat × (1 + Rarity)| Weighted perceptual pop-out                   |
| Color Harmony             | Hue spacing geometry             | Complementary or triadic balance              |
| Composition Bias          | Hue/Sat distribution over layout | Position-aware color imbalance                |
| Dominant Color Regions    | Large clusters with coverage     | Region-level homogeneity                      |

---

## Phase 4: Statistical and Spatial Concepts

| Concept                    | Derived From            | Description                                   |
|----------------------------|--------------------------|-----------------------------------------------|
| Color Clusters             | Hue or a*/b*             | KMeans/VAE palette modeling                   |
| Contextual Importance      | Color + Object/Edge info | Salience modulated by semantic content        |
| Position Weighting         | Color + Grid             | Rule-of-thirds layout heatmap weighting       |
| Contrast Anchors           | High ∇Color in layout zones| Composition-aware tension points             |
| Local Uniformity           | Chroma/Sat patch variance | Smooth vs. rough regional texture             |
| Spatial Harmony            | Hue layout + symmetry     | Balanced chromatic distribution               |

---

## Phase 5: Physical Cues and Integration Concepts

| Concept               | Derived From            | Description                                   |
|------------------------|-------------------------|-----------------------------------------------|
| Luminance Edges        | Gradient of LAB L*      | Brightness transition boundaries              |
| Chromatic Edges        | HSV or LAB gradients    | Edge detection based on color transition      |
| Gradient Magnitudes    | Combined L and a*/b*    | Overall perceptual edge salience              |
| Color–Edge Co-location | Color + edge overlap    | Color–structure interaction zone              |

---

## Roadmap by Tiered Phase

| Tier / Phase                   | Scope                                         |
|--------------------------------|-----------------------------------------------|
| Phase 1: Primary Concepts      | Extract base cues (HSV, LAB, RGB)             |
| Phase 2: Derived Concepts      | Build contrast and differential metrics       |
| Phase 3: Composite Concepts    | Combine cues into salience and harmony models |
| Phase 4: Statistical + Spatial | Analyze layout-aware and semantic properties  |
| Phase 5: Physical + Integration| Model perceptual transitions and fuse with edge/objects |