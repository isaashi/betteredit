# Component → Feature Renaming Guide

This document lists all locations where "component" (referring to Color, Edge, Objects, Saliency) should be renamed to "feature" to align with industry terminology.

**Important**: Only rename "component" when it refers to **Color, Edge, Objects, Saliency** (the image-defining features). Do NOT rename:
- `component` parameter in `DesignRegistry.register()` (refers to registry component, not image component)
- Other uses of "component" in non-image-analysis contexts

---

## CODE FILES

### `src/analyzer/inter_fusion/strategies.py`
- **Line 6**: `"across all final components"` → `"across all final features"`
- **Line 20**: `"normalized component maps"` → `"normalized feature maps"`
- **Line 21**: `"Fuses final components (Color, Edge, Objects, Saliency, etc.)"` → `"Fuses final features (Color, Edge, Objects, Saliency, etc.)"`
- **Line 22**: `"to produce final outputs"` (keep as is)
- **Line 51**: `"normalized component maps"` → `"normalized feature maps"`
- **Line 52**: `"Fuses final components (Color, Edge, Objects, Saliency, etc.)"` → `"Fuses final features (Color, Edge, Objects, Saliency, etc.)"`

---

## DOCUMENTATION FILES

### `docs/neural_inter_fusion_techniques.md`
- **Line 1**: `"Component Map Fusion"` → `"Feature Map Fusion"`
- **Line 3**: `"component maps (Color, Edge, Objects, Saliency, etc.)"` → `"feature maps (Color, Edge, Objects, Saliency, etc.)"`
- **Line 5**: `"image-defining components"` → `"image-defining features"`
- **Line 5**: `"component maps"` → `"feature maps"`
- **Line 12**: `"per-component weights"` → `"per-feature weights"`
- **Line 14**: `"Component maps (Color, Edge, Objects, Saliency)"` → `"Feature maps (Color, Edge, Objects, Saliency)"`
- **Line 15**: `"One weight per component"` → `"One weight per feature"`
- **Line 19**: `"number of components"` → `"number of features"`
- **Line 23**: `"which components are weighted more"` → `"which features are weighted more"`
- **Line 34**: `"per-component importance"` → `"per-feature importance"`
- **Line 36**: `"Component maps (Color, Edge, Objects, Saliency)"` → `"Feature maps (Color, Edge, Objects, Saliency)"`
- **Line 37**: `"gating weights for each component"` → `"gating weights for each feature"`
- **Line 38**: `"how much each component contributes"` → `"how much each feature contributes"`
- **Line 39**: `"combination of components"` → `"combination of features"`
- **Line 44**: `"weight components differently"` → `"weight features differently"`
- **Line 56**: `"each component at each pixel"` → `"each feature at each pixel"`
- **Line 58**: `"Component maps (H×W each)"` → `"Feature maps (H×W each)"`
- **Line 59**: `"processes the component maps"` → `"processes the feature maps"`
- **Line 59**: `"attention maps (H×W) for each component"` → `"attention maps (H×W) for each feature"`
- **Line 60**: `"how important that component is"` → `"how important that feature is"`
- **Line 80**: `"attend to components"` → `"attend to features"`
- **Line 99**: `"Stack component maps"` → `"Stack feature maps"`
- **Line 101**: `"Stack all component maps"` → `"Stack all feature maps"`
- **Line 101**: `"N = number of components"` → `"N = number of features"`
- **Line 103**: `"combine features across components"` → `"combine features across feature types"` (or keep as is if it means combining across different feature maps)
- **Line 109**: `"interactions between components"` → `"interactions between features"`
- **Line 114**: `"which components contribute"` → `"which features contribute"`
- **Line 120**: `"interactions between components"` → `"interactions between features"`
- **Line 122**: `"component features"` → `"feature representations"` (to avoid confusion)
- **Line 140**: `"interactions between components"` → `"interactions between features"`
- **Line 142**: `"component interactions"` → `"feature interactions"`
- **Line 144**: `"how components interact"` → `"how features interact"`
- **Line 161**: `"component relationships"` → `"feature relationships"`
- **Line 163**: `"each component as a 'token'"` → `"each feature as a 'token'"`
- **Line 164**: `"relationships between components"` → `"relationships between features"`
- **Line 165**: `"which components are relevant"` → `"which features are relevant"`
- **Line 171**: `"relationships between components"` → `"relationships between features"`
- **Line 182**: `"One component queries others"` → `"One feature queries others"`
- **Line 185**: `"which other components are relevant"` → `"which other features are relevant"`
- **Line 186**: `"Other components provide"` → `"Other features provide"`
- **Line 203**: `"components as features"` → `"feature types as features"` (or rephrase to avoid confusion)
- **Line 205**: `"component features"` → `"feature representations"`
- **Line 207**: `"component relationships"` → `"feature relationships"`
- **Line 212**: `"component relationships"` → `"feature relationships"`
- **Line 244**: `"components as nodes"` → `"features as nodes"`
- **Line 246**: `"components are nodes"` → `"features are nodes"`
- **Line 247**: `"relationships between components"` → `"relationships between features"`
- **Line 284**: `"which components contribute most"` → `"which features contribute most"`
- **Line 307**: `"components interact"` → `"features interact"`
- **Line 329**: `"Component relationships"` → `"Feature relationships"`

### `docs/fusion_renaming.md`
- **Line 13**: `"within components"` → `"within features"` (in comment about intra-fusion)
- **Line 190**: `"within components"` → `"within features"`
- **Line 191**: `"across components"` → `"across features"`
- **Line 209**: `"within components"` → `"within features"`
- **Line 209**: `"across components"` → `"across features"`

### `docs/next_up.md`
- **Line 8**: `"final component maps (Color, Edge, Objects, Saliency)"` → `"final feature maps (Color, Edge, Objects, Saliency)"`
- **Line 18**: `"[Component Extraction"` → `"[Feature Extraction"`
- **Line 19**: `"Color Component"` → `"Color Feature"`
- **Line 19**: `"Final Color Component"` → `"Final Color Feature"`
- **Line 20**: `"Edge Component"` → `"Edge Feature"`
- **Line 20**: `"Final Edge Component"` → `"Final Edge Feature"`
- **Line 21**: `"Object Component"` → `"Object Feature"`
- **Line 21**: `"Final Object Component"` → `"Final Object Feature"`
- **Line 22**: `"Saliency Component"` → `"Saliency Feature"`
- **Line 22**: `"Final Saliency Component"` → `"Final Saliency Feature"`
- **Line 24**: `"across all components"` → `"across all features"`
- **Line 33**: `"within each component"` → `"within each feature"`
- **Line 34**: `"across all components"` → `"across all features"`

### `docs/protocols.md`
- **Line 21**: `"within a component"` → `"within a feature"`
- **Line 21**: `"final color component"` → `"final color feature"`
- **Line 26**: `"within the component"` → `"within the feature"`
- **Line 33**: `"within a component"` → `"within a feature"`
- **Line 33**: `"of that component"` → `"of that feature"`
- **Line 35**: `"across all components"` → `"across all features"`
- **Line 35**: `"Color, Edge, Objects, Saliency, etc."` (keep as is - these are feature names)
- **Line 100**: `"component names (e.g., "color", "edge", "objects", "saliency")"` → `"feature names (e.g., "color", "edge", "objects", "saliency")"`
- **Line 100**: `"Final Color Component"` → `"Final Color Feature"`
- **Line 100**: `"Final Edge Component"` → `"Final Edge Feature"`
- **Line 103**: `"across all components"` → `"across all features"`
- **Line 103**: `"Color, Edge, Objects, Saliency components"` → `"Color, Edge, Objects, Saliency features"`

### `docs/architecture_understanding.md`
- **Line 9**: `"Multiple Image-Defining Components"` → `"Multiple Image-Defining Features"`
- **Line 11**: `"multiple components"` → `"multiple features"`
- **Line 20**: `"Color and Edge are implemented. Objects and Saliency are planned"` (keep feature names as is)
- **Line 24**: `"Within Each Component"` → `"Within Each Feature"`
- **Line 26**: `"Each component has"` → `"Each feature has"`
- **Line 28**: `"Color Component Example:"` → `"Color Feature Example:"`
- **Line 35**: `"Edge Component Example:"` → `"Edge Feature Example:"`
- **Line 48**: `"Within Each Component"` → `"Within Each Feature"`
- **Line 50**: `"within a single component"` → `"within a single feature"`
- **Line 50**: `"final component representation"` → `"final feature representation"`
- **Line 53**: `"within a component"` → `"within a feature"`
- **Line 54**: `"within a component"` → `"within a feature"`
- **Line 56**: `"Color Component"` → `"Color Feature"`
- **Line 67**: `"Final Color Component"` → `"Final Color Feature"`
- **Line 70**: `"Edge Component"` → `"Edge Feature"`
- **Line 80**: `"Final Edge Component"` → `"Final Edge Feature"`
- **Line 85**: `"Across All Components"` → `"Across All Features"`
- **Line 87**: `"all final components"` → `"all final features"`
- **Line 90**: `"all final components"` → `"all final features"`
- **Line 95**: `"Final Color Component"` → `"Final Color Feature"`
- **Line 96**: `"Final Edge Component"` → `"Final Edge Feature"`
- **Line 97**: `"Final Object Component"` → `"Final Object Feature"`
- **Line 98**: `"Final Saliency Component"` → `"Final Saliency Feature"`
- **Line 99**: `"... (other components)"` → `"... (other features)"`
- **Line 118**: `"[Component Extraction"` → `"[Feature Extraction"`
- **Line 119**: `"Color Component"` → `"Color Feature"`
- **Line 122**: `"Final Color Component"` → `"Final Color Feature"`
- **Line 124**: `"Edge Component"` → `"Edge Feature"`
- **Line 127**: `"Final Edge Component"` → `"Final Edge Feature"`
- **Line 129**: `"Object Component"` → `"Object Feature"`
- **Line 132**: `"Final Object Component"` → `"Final Object Feature"`
- **Line 134**: `"Saliency Component"` → `"Saliency Feature"`
- **Line 137**: `"Final Saliency Component"` → `"Final Saliency Feature"`
- **Line 139**: `"across all components"` → `"across all features"`
- **Line 140**: `"Fused Multi-Component Representation"` → `"Fused Multi-Feature Representation"`
- **Line 143**: `"Inter-Fusion(Color, Edge, Objects, Saliency, ...)"` (keep feature names as is)
- **Line 161**: `"Each component (Color, Edge, Objects, etc.)"` → `"Each feature (Color, Edge, Objects, etc.)"`
- **Line 162**: `"Components follow"` → `"Features follow"`
- **Line 163**: `"→ final component"` → `"→ final feature"`
- **Line 163**: `"Components are then"` → `"Features are then"`
- **Line 170**: `"within a single component"` → `"within a single feature"`
- **Line 172**: `"across all components"` → `"across all features"`
- **Line 174**: `"A major image-defining aspect (Color, Edge, Objects, Saliency, etc.)"` → `"A major image-defining aspect (Color, Edge, Objects, Saliency, etc.)"` (keep as is - this is a definition)
- **Line 183**: `"Color Component"` → `"Color Feature"`
- **Line 184**: `"Edge Component"` → `"Edge Feature"`
- **Line 185**: `"Object Component"` → `"Object Feature"`
- **Line 186**: `"Saliency Component"` → `"Saliency Feature"`

### `docs/fusion_architecture_flow.md`
- **Line 6**: `"[Component Extraction"` → `"[Feature Extraction"`
- **Line 7**: `"Color Component"` → `"Color Feature"`
- **Line 10**: `"Final Color Component"` → `"Final Color Feature"`
- **Line 12**: `"Edge Component"` → `"Edge Feature"`
- **Line 15**: `"Final Edge Component"` → `"Final Edge Feature"`
- **Line 17**: `"Object Component"` → `"Object Feature"`
- **Line 18**: `"Final Object Component"` → `"Final Object Feature"`
- **Line 20**: `"Saliency Component"` → `"Saliency Feature"`
- **Line 21**: `"Final Saliency Component"` → `"Final Saliency Feature"`
- **Line 23**: `"across all components"` → `"across all features"`
- **Line 24**: `"Fused Multi-Component Representation"` → `"Fused Multi-Feature Representation"`

---

## SUMMARY

**Total Changes**:
- **Code Files**: 1 file (`src/analyzer/inter_fusion/strategies.py`) - 6 locations
- **Documentation Files**: 6 files - ~100+ locations

**Key Patterns**:
- "component" → "feature" (when referring to Color, Edge, Objects, Saliency)
- "component maps" → "feature maps"
- "components" → "features" (plural)
- "Component" → "Feature" (capitalized in titles/headers)
- "Color Component" → "Color Feature"
- "Final Color Component" → "Final Color Feature"

**Do NOT rename**:
- `component` parameter in `DesignRegistry.register()` (registry component, not image feature)
- Other non-image-analysis uses of "component"

