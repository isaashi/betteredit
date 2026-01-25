## Phase 0: ML Prerequisites for Neural Inter-Fusion (PRIORITY #1)
- **[ESSENTIAL] Problem framing & success metrics**
  - Define success metrics (NSS/KLD/AUC) and constraints (latency, cost)
- **[ESSENTIAL] Data sourcing**
  - Download MIT1003 and SALICON datasets
  - Add data validation checks during ingestion
- **[ESSENTIAL] Data storage & schema**
  - Organize datasets (`data/raw/`, `data/processed/`)
  - Document dataset schema and splits
- **[ESSENTIAL] Label validation**
  - Verify saliency map alignment and quality
- **[ESSENTIAL] Feature engineering finalization**
  - Normalize/resize feature maps, stack channels, avoid leakage (fit on train only)

## Phase 1: Inter-Fusion Integration & Training (PRIORITY #2)
- **[ESSENTIAL] Inter-Fusion strategy selection**
  - Integrate `WeightedFusion`/`SumFusion` into pipeline (currently unused)
  - Implement factory/selector for Classical vs Neural based on `inter_fusion_strategy`
  - Update pipeline to pass final component maps to selected strategy
  - Add config options for classical inter-fusion (weights, strategy selection)
  - Add validation and error handling (missing model files, untrained model)
  - Test and validate that inter-fusion produces correct final outputs (Visual Weight Heatmap, Eye Flow Path, etc.)
  - Document how to switch between classical and neural inter-fusion in config
- **[ESSENTIAL] Neural Inter-Fusion implementation**
  - Complete `AttentionBasedFusion.fuse()`, `train()`, `load_model()`, `save_model()`
  - Train on visual weight datasets (MIT1003, SALICON) and validate performance improvements over classical inter-fusion
  - Evaluate against target metrics and record baselines

### **Hybrid Architecture Flow:**
```
Input Image
    ↓
[Component Extraction - Each with Classical + Neural sub-components]
    ├─ Color Component → Classical Intra-Fusion → Final Color Component
    ├─ Edge Component → Classical Intra-Fusion → Final Edge Component
    ├─ Object Component (planned) → Classical Intra-Fusion → Final Object Component
    └─ Saliency Component (planned) → Classical Intra-Fusion → Final Saliency Component
    ↓
[Inter-Fusion - Classical or Neural (configurable, SELECT one) across all components]
    ↓
[Final Output Generation]
    ├─ Visual Weight Heatmap
    ├─ Eye Flow Path Overlay
    └─ ... (other outputs)

```

**Key Concepts**:
- **Classical Intra-Fusion**: Rule-based fusion within each component
- **Classical Inter-Fusion**: Rule-based fusion across all components (WeightedFusion/SumFusion)
- **Neural Inter-Fusion**: Learned fusion across all components
- **Goal**: Optimal combination - each output is a single fused result. Selection between Classical and Neural Inter-Fusion is configurable.

**Important Note**: The current design is to **SELECT** either classical OR neural inter-fusion via configuration (`inter_fusion_strategy: "classical" | "neural"`), not combine both. The factory/selector pattern chooses one strategy. Combining both outputs (e.g., ensemble approach) could be a future enhancement, but it's not in the current implementation plan.

**See**: `docs/architecture_understanding.md` for complete architecture overview.

## Phase 2: Streamline Workspace Setup (project.toml - poetry)
- **[ESSENTIAL] Input validation and security**: File type validation and sanitization, path traversal protection, file size limits, resource constraints, sandboxing
- **[ESSENTIAL] Standardize configuration management**: Environment-specific configs (dev/staging/prod), validation strategy, secrets management, hot-reloading

## Phase 3: CLI Entrypoint & Report Export (inc. Logging / Error Handling)
- **[ESSENTIAL] Implement proper layered architecture**
  - Separate domain, application, and infrastructure layers
  - Move pipeline.py to appropriate application layer
  - Implement dependency injection container
  - Add proper abstraction boundaries
- **[ESSENTIAL] Error handling**
  - Wrap main commands in try/except: handle missing EXIF, blank images, model-load failures, invalid configs
  - Implement comprehensive exception hierarchy
  - Add graceful degradation strategies
  - Implement error recovery mechanisms
- **[ESSENTIAL] Implement structured logging**
  - Replace mixed logging frameworks with consistent approach
  - Add log levels configuration
  - Implement metrics collection
  - Add distributed tracing capabilities
- **[ESSENTIAL] ReportGenerator**
  - Ensure support for exporting heatmaps, flow maps, overlays, and JSON summaries
- **[IMPROVEMENT] Disable report.json creation for cli analysis**
- **[IMPROVEMENT] The CLI was designed for analysis (which needs config flexibility, session tracking, etc.) but then benchmarking was shoehorned into the same complex framework. (Logging, Config Loading, Session-based Registry)**
- **[IMPROVEMENT] Cleanup legacy run_analysis.py and run_benchmark.py**
- **[ESSENTIAL] Input validation and security**
  - Add file type validation and sanitization
  - Implement path traversal protection
  - Add file size limits and resource constraints
  - Implement sandboxing for untrusted inputs

## Phase 4: Testing & Fault Tolerance
- **[ESSENTIAL] Establish test categorization**
  - Separate unit, integration, and e2e tests
  - Implement test data management strategy
  - Add comprehensive mocking strategy
  - Implement performance testing framework
- **[ESSENTIAL] Security testing**
  - Test input validation and sanitization
  - Test file type validation
  - Test resource limit enforcement
  - Test error handling for malicious inputs
- **[ESSENTIAL] Integration tests** for end-to-end pipeline
- **[ESSENTIAL] Exception handling** tests for corrupt EXIF, unsupported images, model errors
- **[IMPROVEMENT] Regression tests** comparing saved heatmap/saliency snapshots

## Phase 5: Restructure Tests  
**[ESSENTIAL] Reorganize test structure for maintainability:**
```
tests/
├── test_config/
│   ├── test_settings.py
│   └── test_design_registry.py
├── test_features/
│   ├── test_edge_detector.py
│   ├── test_color_detector.py
│   ├── test_transforms.py
│   └── test_intra_fusion.py
├── test_pipeline/
│   ├── test_feature_extractor.py
│   ├── test_analyzer.py
│   └── test_entrypoints.py
└── test_preprocessing.py
```

## Phase 6: Modernize Project Configuration
- **[ESSENTIAL] Add Docker configuration**: Dockerfile, docker-compose for development, multi-stage builds for production, health checks and monitoring endpoints
- **[ESSENTIAL] GitHub Actions** (or similar) to run: Black, Flake8, mypy, Pytest, optional demo build
- **[ESSENTIAL] Add monitoring and observability**: Health checks, metrics collection (Prometheus), distributed tracing (Jaeger), alerting and notification systems
- **[IMPROVEMENT] Migrate from requirements.txt to pyproject.toml**: Create comprehensive `pyproject.toml` with build system, metadata, dependencies; configure dev tools (black, flake8, mypy, pytest); update installation instructions; remove legacy requirements.txt; add dependency groups (dev, test, docs); configure CLI entry points

## Phase 7: CI/CD Workflow
- **[ESSENTIAL] Architecture documentation**: Layered architecture design, dependency injection patterns, error handling strategies, security considerations
- **[ESSENTIAL] User Guide**: `docs/Getting_Started.md`
- **[IMPROVEMENT] Developer Guide**: `docs/Developer_Guide.md` (protocols, registry, pipeline)
- **[FUTURE] API Reference** via Sphinx once stable

## Phase 8: Documentation
- **[ESSENTIAL] Maintain `CHANGELOG.md`**
- **[ESSENTIAL] Tag **v0.1**; plan **v0.2** for add-ons**
- **[ESSENTIAL] Expose version in `version.py` and `__init__.py`**
- **[ESSENTIAL] Implement semantic versioning**
  - Add version management automation
  - Implement release automation
  - Add changelog generation

## Phase 9: Versioning & Release Strategy
- **[ESSENTIAL] Performance optimization**: Async processing for I/O operations, memory management for large images, resource limits and timeouts, caching strategy
- **[IMPROVEMENT] Extend `benchmarks/runner.py` to discover extractors, log runtime/memory, fusion/report times**
- **[IMPROVEMENT] Store results in CSV/JSON for regression tracking**

## Phase 10: Models & External Dependencies
- **[IMPROVEMENT] Decide hosting (S3/Git LFS)**
- **[IMPROVEMENT] Implement auto-download of missing weights in `core/config.py`**

## Phase 11: Plugin/Extension Pattern
- **[FUTURE] Document "drop-in" plugin folder and decorator registration in Developer Guide**
- **[FUTURE] Logging** - Add `core/log.py` to configure built-in `logging` (replace Loguru)

## Phase 12: Batch & Parallel Processing
- **[FUTURE] Batch support**: folder/queue processing
- **[FUTURE] Parallelism**: `concurrent.futures`/`joblib` per image and across batches
- **[FUTURE] Config**: `batch_size`, `num_workers`

## Phase 13: Performance & Benchmarking Metrics
- **[FUTURE] Unified Testing & Benchmark** (run full benchmark on demand; unify mypy)
- **[FUTURE] Logging & Config Swap** (structlog/logbook; dataclasses+attrs/jsonschema)
- **[FUTURE] Advanced Attention Modeling** (DeepGaze II, SalGAN, attention paths)
- **[FUTURE] Learnable Fusion Strategy** (CNN fusion, training/inference pipelines)
- **[FUTURE] Aesthetic Feedback Engine** (rule-based composition suggestions)
- **[FUTURE] Flow Graph Modeling** (scene graph export to JSON/DOT)
- **[FUTURE] Code quality automation**
  - Implement consistent naming conventions
  - Add code formatting standards enforcement
  - Configure comprehensive linting
  - Establish documentation standards