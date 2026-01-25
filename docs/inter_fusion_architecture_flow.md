# Inter-Fusion Architecture Flow

```
Input Image
    ↓
[Component Extraction - Each with Classical + Neural sub-components]
    ├─ Color Component
    │   ├─ Classical: RGB, HSV, LAB, Hue Contrast, Luminance Contrast
    │   ├─ Neural: Color Clusters (KMeans/VAE), Contextual Importance
    │   └─ → Intra-Fusion (Classical + Neural) → Final Color Component
    │
    ├─ Edge Component
    │   ├─ Classical: Canny, Sobel, Laplacian, Edge Density
    │   ├─ Neural: Semantic Edge Understanding, Flow Linearity
    │   └─ → Intra-Fusion (Classical + Neural) → Final Edge Component
    │
    ├─ Object Component (planned)
    │   └─ → Intra-Fusion → Final Object Component
    │
    └─ Saliency Component (planned)
        └─ → Intra-Fusion → Final Saliency Component
    ↓
[Inter-Fusion - Classical/ Neural (configurable, SELECT one) Fusion across all components]
    └─ → Fused Multi-Component Representation
    ↓
[Final Output Generation]
    ├─ Visual Weight Heatmap
    ├─ Eye Flow Path Overlay
    ├─ Salience Map
    └─ ... (other outputs)

**Note**: Each final output is produced by either classical OR neural inter-fusion (selected via config), not a combination of both. Combining both could be a future enhancement.
```