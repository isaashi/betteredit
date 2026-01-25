# betteredit – Current State

## Overview

**betteredit** is a backend analysis engine designed for integration as a plugin or extension to photo-editing applications (such as Adobe Lightroom). Its goal is to provide overlays and visual feedback that help users edit their photographs more effectively. While the current implementation focuses on the analysis engine and a modern CLI for research and development, the long-term vision is seamless integration with real-world photo-editing UIs. UI integration and direct plugin support are planned for future phases.

---

## Key Features

- **Unified CLI** for single-image analysis and benchmarking, with robust error handling and structured logging.
- **Modular architecture** using protocols/interfaces for color detection, edge detection, fusion, and object/saliency modeling.
- **Configurable pipeline** with YAML-based settings, supporting custom overrides and environment-specific configs.
- **Comprehensive output**: generates overlays, heatmaps, salience maps, and JSON summaries suitable for use in photo-editing workflows. Each final output (Visual Weight Heatmap, Eye Flow Path, etc.) is produced by either classical OR neural inter-fusion (selected via configuration), not a combination of both.
- **Extensive documentation** covering setup, CLI usage, protocols, and model design.

---

## Project Structure

- **src/**: Core codebase (analyzer, features, fusion, report, config, pipeline, CLI)
- **docs/**: Setup, usage, protocols, model design, and roadmap
- **tests/**: Unit, integration, and pipeline tests
- **benchmarking/**: Benchmark datasets and scripts
- **outputs/**: Generated analysis and benchmark results

---

## CLI & User Experience

- **Commands**:  
  - `analyze`: Analyze a single image for visual composition and salience.
  - `benchmark`: Run batch analysis across image sets and strategies.
- **Config**:  
  - Default: `src/betteredit/config/settings.yaml`
  - Custom: User-supplied YAML, deep-merged with defaults.
- **Output**:  
  - Organized by analysis type (color, edge, fusion), with clear directory structure. Outputs are designed to be easily consumed by external UIs or plugins.
- **Error Handling**:  
  - Clear messages for missing files, invalid parameters, and processing errors.
- **Logging**:  
  - Structured logs with session IDs, timestamps, and log levels.

---

## Core Models & Protocols

- **Protocols**:  
  - TypedDict-based schemas for detection results.
  - Standardized interfaces for color/edge detection, fusion, saliency, and object detection.
- **Color Detection**:  
  - Extracts primary (hue, saturation, luminance), derived (contrast, gradients), and composite (salience, rarity, harmony) cues.
  - Multiple fusion strategies: minimal, boosted, full, sum, weighted.
  - Roadmap for data-driven and adaptive fusion.
- **Edge Detection**:  
  - Supports Canny, Sobel, Piotr, Laplacian, and derived features (density, sharpness, orientation).
  - Composite reasoning (salience, contour coherence, anchors).
- **Fusion**:  
  - Pluggable strategies for combining cues, with future support for learned and adaptive fusion.
  - **Inter-Fusion**: The system selects either classical OR neural inter-fusion via configuration (`inter_fusion_strategy: "classical" | "neural"`), not a combination of both. Combining both outputs could be a future enhancement.

---

## Configuration & Setup

- **Modern Python packaging** with `pyproject.toml` (and legacy `requirements.txt` support).
- **Setup**:  
  - Python 3.8+, pip, virtualenv recommended.
  - One-command install and verification.
- **Dependency management**:  
  - Version pinning, OpenCV conflict resolution, and troubleshooting guidance.
- **Platform support**:  
  - macOS, Linux, Windows (WSL recommended).

---

## Testing & Quality

- **Unit and integration tests** for all major modules.
- **Type checking** with mypy.
- **Test structure**:  
  - Organized by feature and pipeline stage.
- **Planned improvements**:  
  - Test categorization, mocking, regression tests, and security testing.

---

## Roadmap & Next Steps

The project is under **active development** with a clear, phased roadmap:

- **Phase 0–1**: Input validation, config management, error handling, logging, and CLI/report improvements.
- **Phase 2–3**: Test infrastructure, security, and maintainability.
- **Phase 4–5**: Dockerization, CI/CD, monitoring, and documentation.
- **Phase 6–12**: Performance, plugin support, batch/parallel processing, advanced modeling, and code quality automation.
- **Future Phase**: UI integration and direct plugin support for photo-editing applications.

See [`docs/next_up.md`](../docs/next_up.md) for detailed priorities and future plans.

---

## Current Limitations

- UI integration and direct plugin support are not yet implemented; current focus is on the backend analysis engine and CLI.
- Some advanced features (sandboxing, distributed tracing, plugin system) are planned but not yet implemented.
- The modern CLI is the primary interface for all analysis and benchmarking tasks. Legacy scripts (run_analysis.py, run_benchmark.py) are retained solely for reference and backward compatibility, however they are slated for deprecation.
- Full production hardening (e.g., Docker, CI/CD, security audits) is in progress.

---

## How to Get Started

- **Setup**: See [`docs/setup.md`](../docs/setup.md) for installation and troubleshooting.
- **Usage**: See [`docs/cli_usage.md`](../docs/cli_usage.md) for CLI commands and configuration.
- **Architecture**: See [`docs/protocols.md`](../docs/protocols.md) for protocol/interface details.
- **Model Design**: See [`docs/color_detection_full_model.md`](../docs/color_detection_full_model.md) and [`docs/edge_detection_full_model.md`](../docs/edge_detection_full_model.md).
- **Roadmap**: See [`docs/next_up.md`](../docs/next_up.md).

---

**This project is designed for extensibility, research, and real-world integration with photo-editing tools.  
If you are reviewing this as a potential employer, please see the roadmap and protocol documentation for a sense of the project’s direction and architecture.**