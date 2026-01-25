#!/usr/bin/env python3
"""
Main entry point for the betteredit package.

This allows the package to be run directly with:
    python -m betteredit
    python -m betteredit analyze --image path/to/image.jpg
    python -m betteredit benchmark --input-dir path/to/images
"""

from .cli import main

if __name__ == "__main__":
    main() 