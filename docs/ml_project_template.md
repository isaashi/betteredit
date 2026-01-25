
## 1. ML Project Lifecycle Applied to Neural Inter-Fusion

### 1.1 Problem Framing & Success Metrics

**ML Template Approach**:
- Define user story and business problem
- Set ML metrics (AUC, MSE, etc.) and business metrics
- Identify constraints: latency, cost, fairness, data availability

**Applied to This Project**:
- **Status**: [PLANNED] Not Started  
- **Estimated Time**: 2-3 hours

**Tasks**:
- Define success metrics:
  - ML Metrics: Correlation with human attention (MIT1003, SALICON), KLD, NSS, AUC
  - Business Metric: Improved visual weight heatmap accuracy vs. classical fusion
- Set constraints:
  - Latency: < 2 seconds per image
  - Cost: Free/cheap datasets, local training preferred
  - Data: MIT1003 (1003 images), SALICON (10K images)

### 1.2 Data Sourcing

**ML Template Approach**:
- Options: APIs, web scraping, custom datasets, niche sources
- Continuous collection: cron jobs, Airflow/Prefect, cloud schedulers
- Data quality checks: field validation, range checks, null detection

**Applied to This Project**:
- **Status**: [PLANNED] Not Started  
- **Estimated Time**: 3-4 hours

**Tasks**:
- Download MIT1003 dataset (eye-tracking ground truth)
- Download SALICON dataset (larger scale, mouse-tracking)
- Set up data collection scripts with validation checks

### 1.3 Data Storage

**ML Template Approach**:
- Structured data: PostgreSQL/MySQL
- Unstructured data: AWS S3 (images, videos, files)
- Advanced: Redis for caching, DVC for data versioning
- Cloud-first approach recommended

**Applied to This Project**:
- **Status**: [PLANNED] Not Started  
- **Estimated Time**: 2-3 hours

**Tasks**:
- Organize datasets: `data/raw/`, `data/processed/`
- Create data schema documentation
- For portfolio: Local storage is fine, document structure

### 1.4 Feature Engineering

**ML Template Approach**:
- Clean: handle missing values, outliers, type conversion
- Create: derive features from timestamps, text embeddings, image features
- Prepare: normalization, scaling (0-1)
- Avoid data leakage: fit scalers on train only
- Feature selection: importance, correlations, recursive elimination

**Applied to This Project**:
- **Status**: [IN PROGRESS] Partially Done  
- **Estimated Time**: 4-6 hours

**Tasks**:
- Extract final feature maps from existing components (Color, Edge)
- Preprocessing: Normalize to [0, 1], resize, stack as channels
- Feature selection: Start with Color + Edge, add Objects/Saliency when available
- Avoid data leakage: Normalization parameters fit on training set only

### 1.5 Labeling

**ML Template Approach**:
- Create labeling guidelines
- Manual labeling (small datasets) or programmatic labeling (large datasets)
- Weak supervision: rule-based heuristics
- LLM-assisted labeling: GPT with prompts
- Validate: manual review, inter-annotator agreement

**Applied to This Project**:
- **Status**: [PLANNED] Not Started (datasets already labeled)  
- **Estimated Time**: 1 hour

**Tasks**:
- MIT1003 and SALICON provide ground truth saliency maps
- Validate ground truth quality and alignment

### 1.6 Model Training & Evaluation

**ML Template Approach**:
- Proper splits: train/validation/test (chronological for time series)
- Experiment tracking: MLflow, Weights & Biases
- Model versioning: model_v1.pkl or model registry
- Evaluation: appropriate metrics, error analysis, segment evaluation

**Applied to This Project**:
- **Status**: [IN PROGRESS]  
- **Estimated Time**: 20-30 hours

**Tasks**:
1. Complete Neural Inter-Fusion Implementation:
   - Complete `AttentionBasedFusion.fuse()` method
   - Implement `train()` method with data loading, loss function, training loop
   - Implement `load_model()` and `save_model()`
   - Start simple: Learned Weighted Sum (#5 from techniques doc)
   - Progress to: Learned Gating (#6) or Spatial Attention (#8)

2. Training Setup:
   - Train/Val/Test splits (80/10/10 or 70/15/15)
   - Experiment tracking: MLflow or simple logging
   - Model versioning: `models/neural_inter_fusion_v1.pth`

3. Evaluation:
   - Primary metric: Correlation with ground truth (KLD, NSS, AUC)
   - Compare against: Classical inter-fusion (WeightedFusion baseline)
   - Segment evaluation: Different image types, compositions

**Reference**: `docs/neural_inter_fusion_techniques.md` (recommended exploration path)

### 1.7 Deployment

**ML Template Approach**:
- REST API: FastAPI/Flask (most professional)
- Batch predictions: Airflow scheduling
- Interactive app: Streamlit/Gradio (quick demo)
- Docker: containerization for reproducibility
- CI/CD: GitHub Actions for automated testing/deployment
- Testing: unit tests, integration tests

**Applied to This Project**:
- **Status**: [PLANNED] Not Started  
- **Estimated Time**: 4-6 hours

**Tasks**:
- CLI Integration (enhance existing)
- Docker (from Phase 5, but can start early)
- Testing: Unit tests, integration tests

### 1.8 Monitoring

**ML Template Approach**:
- Log predictions: timestamp, input features, outputs
- Periodic metrics: weekly accuracy on fresh data
- Data drift checks: unexpected values, null patterns
- Basic infrastructure (dashboards/alerts optional)

**Applied to This Project**:
- **Status**: [PLANNED] Not Started  
- **Estimated Time**: 2-3 hours

**Tasks**:
- Log predictions: Timestamp, input image path, fusion strategy used
- Basic metrics: Track strategy usage, processing times, errors
- For portfolio: Simple logging to file/database is sufficient

---

## 2. ML Steps Dependency Order

```
Problem Framing & Success Metrics
    │
    │ (defines what data to collect)
    ▼
Data Sourcing
    │
    │ (provides data to store)
    ▼
Data Storage
    │
    │ (enables feature access)
    ▼
Feature Engineering
    │
    │ (prepares data for labeling/training)
    ├─→ Labeling (if supervised)
    │       │
    │       │ (provides labels)
    │       ▼
    └─→ Model Training & Evaluation
            │
            │ (produces trained model)
            ▼
        Deployment
            │
            │ (enables monitoring)
            ▼
        Monitoring
            │
            │ (enables feedback loop)
            └─→ Retraining (cycle continues)
```

**Key Dependencies**:
- Problem Framing blocks everything (defines scope)
- Data Sourcing → Data Storage → Feature Engineering (sequential)
- Feature Engineering → Labeling (if needed) → Model Training (sequential)
- Model Training → Deployment → Monitoring (sequential)
- Monitoring enables feedback loop for retraining