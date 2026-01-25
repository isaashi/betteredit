# betteredit - Setup Guide

## Overview

This document provides comprehensive setup instructions for the betteredit project. The project uses modern Python packaging standards with fallback support for legacy systems.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)
- Virtual environment tool (recommended)

## Installation

This method uses the project's `project.toml` configuration file and provides the most reliable setup.

```bash
# Clone the repository
git clone https://github.com/isaashi/betteredit.git
cd betteredit

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Upgrade pip
python3 -m pip install --upgrade pip

# Install in development mode
python3 -m pip install -e .

# Verify installation
betteredit --help
```

## Dependencies

The project uses the following core dependencies:

### Core Dependencies
- Image processing: OpenCV, PIL
- Scientific computing: NumPy, SciPy, scikit-learn
- Visualization: Matplotlib
- Configuration: PyYAML, Pydantic, Loguru

## Configuration

### Environment Variables

The project uses Pydantic Settings for configuration management. Configuration can be specified via:

- Command-line arguments
- Configuration files
- Environment variables (if implemented)

### Configuration Files

Default configuration is loaded from `src/betteredit/config/settings.yaml`. Custom configurations can be specified via command-line arguments.

## Verification

After installation, verify the setup:

```bash
# Check if the command is available
which betteredit

# Test basic functionality
betteredit --help

# Check installed packages
python3 -m pip list | grep betteredit
```

## Testing & Validation

### Type Checking
```bash
mypy --config-file mypy.ini src/betteredit
```

### Unit Tests
```bash
#python -m unittest discover -s tests -p "test*.py"
pytest
```

## Usage Examples
```bash
python src/betteredit/cli.py analyze --image analysis/image_set/poppies.jpg
python src/betteredit/cli.py benchmark
```

## Troubleshooting

### Common Issues

**OpenCV Installation Problems**
```bash
# If OpenCV installation fails, try:
python3 -m pip uninstall opencv-python opencv-python-headless
python3 -m pip install opencv-contrib-python>=4.8.0,<5.0.0
```

**Permission Errors**
```bash
# If you get permission errors, use:
python3 -m pip install --user -e .
```

**Virtual Environment Issues**
```bash
# If virtual environment doesn't activate:
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# If virtual environment is corrupted:
rm -rf venv
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -e .
```

**Missing Dependencies**
```bash
# If some dependencies are missing:
python3 -m pip install --upgrade pip
python3 -m pip install -e . --force-reinstall
```

### Dependency Conflicts

The project resolves several known dependency conflicts:

- **OpenCV**: Uses only `opencv-contrib-python` to avoid conflicts with `opencv-python` and `opencv-python-headless`
- **Version Pinning**: All dependencies have specific version ranges for reproducibility

### Platform-Specific Notes

**macOS**
- No additional system dependencies required

**Linux**
- May require additional system packages for OpenCV
- GPU support depends on CUDA installation

**Windows**
- Use Windows Subsystem for Linux (WSL) for best compatibility
- Ensure Python is added to PATH

## Uninstallation

To remove the project:

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv

# Or uninstall from system Python
python3 -m pip uninstall betteredit
```

## Support

For additional support:

- Check the project documentation in `docs/`
- Review the test suite in `tests/`
- Consult the project roadmap in `docs/next_up.md`
- Report issues on the project repository

## Version Compatibility

This setup guide is compatible with:
- Python 3.8+
- pip 21.0+
- setuptools 61.0+
- All major operating systems (macOS, Linux, Windows)

---

### Legacy Installation

For systems that don't support modern Python packaging:

```bash
# Follow steps 1-4 from Method 1, then:
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

## Testing & Validation

### Type Checking
```bash
mypy --config-file mypy.ini src/betteredit
```

### Unit Tests
```bash
python -m unittest discover -s tests -p "test*.py"
```

## Usage Examples
```bash
./scripts/run_analysis.py
./scripts/run_analysis.py --image analysis/image_set/poppies.jpg
python -m benchmarking.run_benchmark
```