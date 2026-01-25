#!/usr/bin/env python3
"""
Tests for the betteredit CLI functionality (argparse-based).
"""

import os
import sys
import tempfile
import subprocess
import pytest
from unittest.mock import patch, MagicMock

# Add project root to path
BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASEDIR not in sys.path:
    sys.path.insert(0, BASEDIR)

CLI_PATH = os.path.join(BASEDIR, "src", "betteredit", "cli.py")

class TestCLI:
    """Test cases for CLI functionality (argparse-based)."""

    def test_cli_help(self):
        """Test that CLI help works."""
        result = subprocess.run([sys.executable, CLI_PATH, '--help'], capture_output=True, text=True)
        assert result.returncode == 0
        assert "betteredit" in result.stdout
        assert "analyze" in result.stdout
        assert "benchmark" in result.stdout

    def test_analyze_help(self):
        """Test that analyze command help works."""
        result = subprocess.run([sys.executable, CLI_PATH, 'analyze', '--help'], capture_output=True, text=True)
        assert result.returncode == 0
        assert "Analyze a single image" in result.stdout
        assert "--image" in result.stdout
        assert "--config" in result.stdout
        assert "--output-dir" in result.stdout

    def test_benchmark_help(self):
        """Test that benchmark command help works."""
        result = subprocess.run([sys.executable, CLI_PATH, 'benchmark', '--help'], capture_output=True, text=True)
        assert result.returncode == 0
        assert "Benchmark a set of images" in result.stdout
        assert "--input-dir" in result.stdout
        assert "--output-dir" in result.stdout
        assert "--target-size" in result.stdout

    @patch('src.betteredit.cli.process_single_image')
    @patch('src.betteredit.cli.DesignRegistry')
    @patch('src.betteredit.cli.setup_logging')
    @patch('src.betteredit.cli.load_settings')
    @patch('argparse.ArgumentParser.parse_args')
    def test_analyze_command_success(self, mock_parse_args, mock_load_settings, mock_logging, mock_registry, mock_process, tmp_path):
        """Test successful analyze command execution - verifies logging, registry, and settings loading."""
        # Mock setup
        mock_cfg = MagicMock()
        mock_cfg.output_dir = str(tmp_path)
        mock_cfg.model_dump.return_value = {"test": "config"}
        mock_load_settings.return_value = mock_cfg
        mock_logging.return_value = "test-session-id"
        mock_process.return_value = {"status": "success"}

        # Use a real image from benchmarking folder
        benchmark_image_dir = os.path.join(BASEDIR, "benchmarking", "image_set")
        test_images = [f for f in os.listdir(benchmark_image_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        if not test_images:
            pytest.skip("No test images found in benchmarking/image_set")
        test_image_path = os.path.join(benchmark_image_dir, test_images[0])

        # Mock argparse to return analyze command arguments
        mock_args = MagicMock()
        mock_args.command = "analyze"
        mock_args.image = test_image_path
        mock_args.config = None
        mock_args.output_dir = str(tmp_path)
        mock_parse_args.return_value = mock_args

        # Call main() directly (not via subprocess) so mocks work
        from src.betteredit.cli import main
        main()

        # Verify all components were called correctly
        mock_load_settings.assert_called_once_with(
            config_path=None,
            image_path=test_image_path,
            output_dir=str(tmp_path)
        )
        mock_logging.assert_called_once()
        mock_registry.start_session.assert_called_once_with("test-session-id", {"test": "config"})
        mock_process.assert_called_once()

    def test_analyze_command_integration(self, tmp_path):
        """Integration test: Test analyze command end-to-end via subprocess."""
        # Use a real image from benchmarking folder
        benchmark_image_dir = os.path.join(BASEDIR, "benchmarking", "image_set")
        test_images = [f for f in os.listdir(benchmark_image_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        if not test_images:
            pytest.skip("No test images found in benchmarking/image_set")
        test_image_path = os.path.join(benchmark_image_dir, test_images[0])

        # Run command via subprocess (end-to-end test, no mocks)
        result = subprocess.run([
            sys.executable, CLI_PATH,
            'analyze',
            '--image', test_image_path,
            '--output-dir', str(tmp_path)
        ], capture_output=True, text=True)

        # Verify command succeeded
        assert result.returncode == 0, f"CLI failed with stderr: {result.stderr}"
        # Verify output directory was created
        assert os.path.exists(tmp_path), "Output directory should be created"
        # Verify registry file was created
        registry_path = os.path.join(tmp_path, "analysis_design_registry.json")
        assert os.path.exists(registry_path), "Design registry should be created"

    @patch('src.betteredit.cli.load_settings')
    @patch('src.betteredit.cli.setup_logging')
    @patch('src.betteredit.cli.DesignRegistry')
    def test_analyze_command_missing_image(self, mock_registry, mock_logging, mock_load_settings, tmp_path):
        """Test analyze command with missing image file."""
        # Mock setup
        mock_load_settings.return_value = MagicMock()
        mock_logging.return_value = "test-session-id"

        # Run command with non-existent image
        result = subprocess.run([
            sys.executable, CLI_PATH,
            'analyze',
            '--image', '/non/existent/image.jpg',
            '--output-dir', str(tmp_path)
        ], capture_output=True, text=True)

        # Verify - errors are logged to stderr, not stdout
        assert result.returncode == 1
        assert "failed" in result.stderr.lower() or "error" in result.stderr.lower() or "not found" in result.stderr.lower()

    def test_load_settings_success(self):
        """Test successful settings loading."""
        # This test would require a valid config file
        # For now, we'll test the function signature and basic structure
        from src.betteredit.cli import load_settings
        with patch('src.betteredit.cli.DEFAULT_CONFIG_PATH', '/fake/path'):
            with pytest.raises(FileNotFoundError):
                load_settings()

    def test_setup_logging(self):
        """Test logging setup."""
        from src.betteredit.cli import setup_logging
        session_id = setup_logging()
        assert isinstance(session_id, str)
        assert len(session_id) > 0

if __name__ == "__main__":
    pytest.main([__file__])