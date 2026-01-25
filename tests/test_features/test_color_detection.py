import os
import unittest
import numpy as np

from src.betteredit.config import Settings, ColorDetectionConfig
from src.analyzer.preprocessing import preprocess_image
from src.analyzer.features.color_detection.base import ColorDetector


class TestColorDetector(unittest.TestCase):

    def setUp(self):
        # Load full Settings and pull out the ColorDetectionConfig
        settings = Settings.load()
        self.color_cfg: ColorDetectionConfig = settings.color_detection

        # Prepare test image - check IMAGE_PATH env var, fallback to benchmarking/image_set
        env_path = os.getenv("IMAGE_PATH")
        if env_path and os.path.exists(env_path):
            self.image_path = env_path
        else:
            # fallback to first image in benchmarking/image_set
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "benchmarking", "image_set"))
            images = [f for f in os.listdir(base_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
            if images:
                self.image_path = os.path.join(base_dir, images[0])
            else:
                raise FileNotFoundError(f"No test images found in {base_dir}")

        size_str = os.environ.get("TARGET_SIZE", "224,224")
        w, h = map(int, size_str.split(","))
        self.target_size = (w, h)

        self.image_data = preprocess_image(self.image_path, self.target_size)
        self.detector = ColorDetector(self.color_cfg)

    def test_return_structure(self):
        result = self.detector.detect(self.image_data)
        # Must have top-level cues and combined
        self.assertIn("cues", result)
        self.assertIn("combined", result)

        cues = result["cues"]
        combined = result["combined"]

        # Check each cue block (raw + derived)
        expected_cues = [
            "hue", "saturation", "luminance", "rarity",
            "hue_contrast", "luminance_contrast"
        ]
        for key in expected_cues:
            self.assertIn(key, cues, msg=f"Missing cue block: {key}")
            block = cues[key]
            self.assertIsInstance(block, dict)
            for subkey in ["map", "density", "salience"]:
                self.assertIn(subkey, block, msg=f"{key} block missing '{subkey}'")
                arr = block[subkey]
                self.assertIsInstance(arr, np.ndarray)
                self.assertEqual(arr.shape, self.image_data["rgb"]["og"].shape[:2])
                self.assertTrue(np.issubdtype(arr.dtype, np.floating))

        # Check combined outputs
        for subkey in ["strength", "density", "salience"]:
            self.assertIn(subkey, combined, msg=f"Combined missing '{subkey}'")
            arr = combined[subkey]
            self.assertIsInstance(arr, np.ndarray)
            self.assertEqual(arr.shape, self.image_data["rgb"]["og"].shape[:2])

    def test_salience_range(self):
        result = self.detector.detect(self.image_data)
        sal = result["combined"]["salience"]
        self.assertGreaterEqual(sal.min(), 0.0)
        self.assertLessEqual(sal.max(), 1.0)

    def test_no_nans(self):
        result = self.detector.detect(self.image_data)
        # No NaNs in cues
        for block in result["cues"].values():
            for arr in block.values():
                self.assertFalse(np.isnan(arr).any(), "NaNs found in cue block")
        # No NaNs in combined
        for arr in result["combined"].values():
            self.assertFalse(np.isnan(arr).any(), "NaNs found in combined block")

    def test_color_detector_configurable(self):
        # Build a minimal override config
        override = {
            "salience_strategy": "weighted",
            "contrast_method": "combined",
            "sobel_weight": 0.6,
            "rarity_space": "lab",
            "rarity_k": 10,
            "weights": {"hue": 0.1, "sat": 0.3, "rarity": 0.2, "lum": 0.4},
            "return_density": False,
            "return_salience": True,
            "density_window_size": 12
        }
        cd_cfg = ColorDetectionConfig(**{**self.color_cfg.model_dump(), **override})
        detector = ColorDetector(cd_cfg)

        self.assertEqual(detector.salience_strategy, "weighted")
        self.assertEqual(detector.rarity_k, 10)
        self.assertEqual(detector.sobel_weight, 0.6)
        self.assertEqual(detector.weights["lum"], 0.4)
        # Overridden flags
        self.assertFalse(detector.return_density)
        self.assertTrue(detector.return_salience)


if __name__ == "__main__":
    unittest.main()