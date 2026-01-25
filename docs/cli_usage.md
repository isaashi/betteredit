# betteredit CLI Usage

## Overview

The betteredit now provides a unified command-line interface that combines both single image analysis and benchmarking functionality. The CLI is built using Click and provides a modern, user-friendly interface.

## Installation

Make sure you have the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Commands

The CLI provides two main commands:

1. **`analyze`** - Analyze a single image for visual composition and weight
2. **`benchmark`** - Run benchmarking across multiple images and strategies

### Getting Help

```bash
# General help
python -m betteredit --help

# Command-specific help
python -m betteredit analyze --help
python -m betteredit benchmark --help

# Version information
python -m betteredit --version
```

## Single Image Analysis

### Basic Usage

```bash
# Analyze a single image using default settings
python -m betteredit analyze --image path/to/image.jpg

# Specify output directory
python -m betteredit analyze --image path/to/image.jpg --output-dir ./results

# Use custom configuration
python -m betteredit analyze --image path/to/image.jpg --config my_config.yaml
```

### Options

- `--image, -i`: Path to input image file (overrides `image_path` in settings.yaml)
- `--config, -c`: Path to user-supplied YAML config override
- `--output-dir, -o`: Directory for output files (overrides `output_dir` in settings)

### Example

```bash
python -m betteredit analyze \
    --image /path/to/landscape.jpg \
    --output-dir ./analysis_results \
    --config custom_settings.yaml
```

## Benchmarking

### Basic Usage

```bash
# Run benchmark with default settings
python -m betteredit benchmark

# Specify custom input/output directories
python -m betteredit benchmark \
    --input-dir ./my_images \
    --output-dir ./benchmark_results

# Use custom target size
python -m betteredit benchmark \
    --target-size 512,512
```

### Options

- `--config, -c`: Path to user-supplied YAML config override
- `--input-dir, -i`: Directory containing images to benchmark (default: `benchmarking/image_set`)
- `--output-dir, -o`: Directory for benchmark outputs (default: `benchmarking/outputs`)
- `--target-size, -s`: Target size as W,H (default: `224,224`)

### Example

```bash
python -m betteredit benchmark \
    --input-dir ./test_images \
    --output-dir ./results \
    --target-size 512,224 \
    --config benchmark_config.yaml
```

## Configuration

### Default Configuration

The CLI uses the default configuration from `src/betteredit/config/settings.yaml`.

### Custom Configuration

You can provide a custom YAML configuration file that will be deep-merged with the default configuration:

```yaml
# my_config.yaml
image_path: /path/to/default/image.jpg
target_size: [512, 224]
save_visuals: true
output_dir: ./my_outputs

edge_detection:
  methods: [canny, sobel]
  fusion_strategy: weighted
  fusion_weights:
    canny: 0.7
    sobel: 0.3

color_detection:
  salience_strategy: weighted
  weights:
    hue: 0.2
    sat: 0.3
    rarity: 0.2
    lum: 0.3
```

### Configuration Precedence

1. Default configuration (`settings.yaml`)
2. User configuration file (`--config`)
3. CLI overrides (`--image`, `--output-dir`)

## Output Structure

### Single Image Analysis

```
output_dir/
├── color_detection/
│   ├── image_hue.png
│   ├── image_saturation.png
│   ├── image_luminance.png
│   ├── image_hue_contrast.png
│   ├── image_luminance_contrast.png
│   ├── image_rarity.png
│   └── image_salience.png
├── edge_detection/
│   ├── image_canny_edge_map.png
│   ├── image_canny_edge_density.png
│   ├── image_canny_edge_salience.png
│   ├── image_sobel_edge_map.png
│   ├── image_sobel_edge_density.png
│   ├── image_sobel_edge_salience.png
│   ├── image_fused_edge_strength.png
│   ├── image_fused_edge_density.png
│   └── image_fused_edge_salience.png
└── design_registry.json
```

### Benchmarking

```
output_dir/
├── image1_minimal_hue.png
├── image1_minimal_saturation.png
├── image1_minimal_luminance.png
├── image1_boosted_hue.png
├── image1_boosted_saturation.png
├── image1_boosted_luminance.png
├── image1_full_hue.png
├── image1_full_saturation.png
├── image1_full_luminance.png
├── image1_sum_hue.png
├── image1_sum_saturation.png
├── image1_sum_luminance.png
├── image1_weighted_hue.png
├── image1_weighted_saturation.png
├── image1_weighted_luminance.png
├── image1_benchmark_report.json
├── image2_minimal_hue.png
├── ...
└── design_registry.json
```

## Error Handling

The CLI provides comprehensive error handling:

- **Missing files**: Clear error messages for missing images, config files, or directories
- **Invalid parameters**: Validation of target sizes, file paths, and configuration
- **Processing errors**: Graceful handling of analysis failures with detailed logging

## Logging

The CLI uses structured logging with:

- Session IDs for tracking individual runs
- Timestamped log entries
- Different log levels (INFO, DEBUG, ERROR)
- Design registry integration for audit trails

## Integration with Existing Scripts

The new CLI replaces the functionality of:
- `scripts/run_analysis.py`
- `benchmarking/run_benchmark.py`

The old scripts can still be used for backward compatibility, but the new CLI provides a more consistent and user-friendly interface.

## Examples

### Quick Start

```bash
# Analyze a single image
python -m betteredit analyze -i my_photo.jpg -o ./results

# Run benchmark on test images
python -m betteredit benchmark -i ./test_images -o ./benchmark_results
```

### Advanced Usage

```bash
# Custom configuration with specific parameters
python -m betteredit analyze \
    --image landscape.jpg \
    --config high_res_config.yaml \
    --output-dir ./high_res_analysis

# Benchmark with custom size and configuration
python -m betteredit benchmark \
    --input-dir ./dataset \
    --output-dir ./results \
    --target-size 1024,512 \
    --config benchmark_config.yaml
``` 