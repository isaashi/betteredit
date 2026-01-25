# Feature → Prediction Renaming Guide

This document lists all locations where "feature" (referring to final outputs like Visual Weight Heatmap, Eye Flow Path, etc.) should be renamed to "prediction" to align with industry terminology.

**Important**: Only rename "feature" when it refers to **final outputs/predictions**. Do NOT rename:
- "feature extraction" (correct industry term)
- "feature maps" (correct industry term for intermediate representations)
- "features" as a variable name for extracted data (e.g., `features = extractor.extract()`)
- "FeatureExtractor" class name
- "features/" directory name

---

## DOCUMENTATION FILES

### `docs/inter_fusion_full_model.md`
- **Line 1**: Table header `| Feature |` → `| Prediction |`
  - **Context**: The table lists final outputs (Visual Weight Heatmap, Eye Flow Path, etc.), not intermediate features
  - **Rationale**: These are predictions/outputs, not input features

---

## CODE FILES

**Note**: After careful review, the codebase uses "feature" correctly:
- `FeatureExtractor` - correct (extracts features from images)
- `features = extractor.extract()` - correct (returns feature maps from components)
- `feature_map` variables - correct (referring to intermediate feature maps)
- "feature extraction" - correct industry term

**No code changes needed** - the codebase already uses "feature" correctly for intermediate processing and "features" correctly for the extracted component maps.

---

## SUMMARY

**Total Changes**: 1 location
- 1 documentation file (table header)

**Rationale**: The only place where "feature" incorrectly refers to final outputs is in the table header of `inter_fusion_full_model.md`. All other uses of "feature" in the codebase correctly refer to intermediate features, feature extraction, or feature maps, which are standard industry terms.

