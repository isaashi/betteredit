# Color Detection Fusion Weights Strategy

This document outlines how different visual cues (e.g., hue contrast, saturation, rarity, luminance contrast) should be weighed and combined within the Color component to generate color salience maps. This is **Classical Intra-Fusion** (fusion within the Color component).

---

## 1. Current State

The current engine supports five fusion strategies:
- `minimal`: basic multiplicative model (hue × saturation)
- `boosted`: adds rarity boost
- `full`: includes luminance contrast
- `sum`: additive average of all cues
- `weighted`: explicit control over cue weights

The `"sum"` strategy has proven empirically strong across a wide benchmark (18 images or architecture, landscape, nature and people). `"weighted"` will allow cue importance to be fine-tuned and eventually learned.

| Cue               | Weight |
|------------------|--------|
| Hue Contrast      | 0.1    |
| Saturation        | 0.3    |
| Color Rarity      | 0.2    |
| Luminance Contrast| 0.4    |

---

## 2. Mid-Term Goal: Data-Driven Weight Learning

### Objective:
Replace manual tuning with learned weights from data.

### Approaches:
- **Linear Regression**: Learn scalar weights from training salience scores.
- **Ridge / Lasso**: Add regularization for stability or sparsity.
- **Shallow MLP**: Learn nonlinear cue fusion patterns.

### Inputs:
- Global or patchwise statistics for: hue contrast, saturation, rarity, luminance
- Image category or layout metadata (optional)

### Targets:
- Eye-tracking salience maps
- Manually annotated attention heatmaps
- Synthetic targets in absence of real data

---

## 3. Long-Term Goal: Adaptive or Learned Spatial Fusion

### Objective:
Move beyond global scalar weights toward per-pixel or context-aware fusion.

### Possibilities:
- **Spatial Gating**: Weight maps learned for each cue over image grid
- **Attention Fusion**: Cue importance conditioned on local visual content
- **End-to-End Models**: CNN or transformer-based models that ingest cue stacks and produce salience maps

### Requirements:
- Rich annotated datasets
- Differentiable fusion pipelines
- Possibly pretrained perceptual models (e.g., vision transformers, SAM, DeepGaze)