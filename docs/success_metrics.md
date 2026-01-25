# Success Metrics & Evaluation Plan

This document defines the problem framing, success metrics, and measurement plan for
the betteredit, with a focus on inter-fusion outcomes and saliency prediction.
It consolidates goals and constraints referenced across the project docs and makes them
actionable for evaluation.

---

## 1. Problem Framing (Finalized)

Build a visual analysis engine that predicts human attention and composition cues from
images, producing outputs like Visual Weight Heatmaps, Eye Flow Paths, and Salience Maps.
The system uses a two-level fusion architecture:

- **Intra-Fusion**: classical (rule-based) fusion within each feature (Color, Edge, etc.)
- **Inter-Fusion**: classical OR neural fusion across features (select one per run)

**Goal**: Improve attention prediction quality beyond classical inter-fusion while
remaining fast and usable in interactive workflows and CLI usage.

---

## 2. Success Metrics (Core)

### 2.1 Primary ML Metrics (Saliency Ground Truth)
Use human-attention datasets (MIT1003, SALICON) to evaluate per-image saliency maps:

- **NSS (Normalized Scanpath Saliency)**: correlation with human fixation points
- **KLD (Kullback-Leibler Divergence)**: distribution similarity to ground truth
- **AUC (Area Under Curve)**: saliency ranking vs. human fixations

**Target (relative)**:
- Improve **NSS** and **AUC**, reduce **KLD** versus classical inter-fusion baseline.

### 2.2 Primary Business Metric
- **Improved accuracy vs. classical inter-fusion baseline** (WeightedFusion/SumFusion).

This is the core "win condition" for neural inter-fusion adoption.

---

## 3. Operational Constraints

These constraints are required for practical use in CLI and future UI integrations.

- **Latency**: < 2 seconds per image (single-image analysis target)
- **Cost**: Prefer free/low-cost datasets and local training
- **Data**: MIT1003 (~1003 images), SALICON (~10K images)

---

## 4. Measurement Plan (Evaluation Protocol)

### 4.1 Baseline Definition
Establish a strong baseline before training:

- **Baseline**: Classical inter-fusion (WeightedFusion or SumFusion)
- Evaluate baseline on MIT1003 + SALICON using NSS/KLD/AUC
- Record per-dataset and per-category results

### 4.2 Dataset Splits
Standard supervised split:

- Train / Val / Test = **70/15/15** or **80/10/10**
- Fit normalization/statistics on train only to avoid leakage

### 4.3 Reporting Structure
Report metrics in a consistent table:

- Dataset → NSS, AUC, KLD
- Model → Baseline vs Neural Inter-Fusion
- Delta vs Baseline (%) and absolute

---

## 5. Targets & Thresholds (Suggested)

### 5.1 Relative Improvement (Recommended)
Set targets as improvements over baseline:

- **NSS**: +5% (or +0.05 absolute)
- **AUC**: +1–3%
- **KLD**: −10%

### 5.2 Absolute Thresholds (Directional)
Use only as guidance, since ranges vary by dataset:

- NSS > 1.5
- AUC > 0.80
- KLD < 1.0

---

## 6. Success Gate

Neural inter-fusion is considered successful if:

- **NSS and AUC improve** and **KLD decreases** vs baseline
- **Latency** remains < 2 seconds per image
- No regressions in stability (NaNs, missing outputs, crashes)

---

## 7. Practical Path to Hitting Targets

### 7.1 Start Simple
Begin with low-complexity neural fusion:

- **Learned Weighted Sum** (baseline neural)
- **Learned Gating** (input-adaptive)

These are interpretable and likely to beat classical baselines on small datasets.

### 7.2 Escalate Only If Needed
If gains are weak, progress to:

- **Spatial Attention**
- **Concatenation + CNN**
- **Self-Attention Fusion**

### 7.3 Evaluation Ladder
Use staged validation to prevent overfitting:

1. Beat baseline on **NSS**
2. Beat baseline on **NSS + AUC**, reduce **KLD**
3. Maintain gains while meeting latency constraints

---

## 8. Metrics for Non-Saliency Outputs (Optional Extensions)

Some outputs (e.g., Eye Flow Path, Visual Hierarchy) may need additional measures:

- **Eye Flow Path**: sequence similarity to eye-tracking scanpaths
- **Visual Hierarchy**: rank correlation (Spearman) with human importance ratings
- **Balance/Rhythm**: agreement with human judgments or expert annotations

These are secondary and can be added as additional benchmarks.

---

## 9. Notes on Fusion Strategy Selection

The current system **selects either classical OR neural inter-fusion per run**.
Combining outputs (ensemble) is explicitly deferred to future work.

---

## 10. Recommended Artifacts to Store

- `baseline_metrics.json` (per dataset)
- `neural_metrics.json` (per dataset)
- `evaluation_report.md`
- `model_card.md` (model architecture, data, metrics, limits)