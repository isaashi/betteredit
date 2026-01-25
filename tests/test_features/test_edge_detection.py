
import os
import unittest
import numpy as np

from src.betteredit.config import ColorDetectionConfig, EdgeDetectionConfig, Settings
from src.analyzer.preprocessing import preprocess_image
from src.analyzer.features.edge_detection.base import EdgeDetector
from src.analyzer.features.base import FeatureExtractor


class TestEdgeDetection(unittest.TestCase):
    def setUp(self):
        # Load and validate config
        settings = Settings.load()
        self.color_cfg: ColorDetectionConfig = settings.color_detection
        self.edge_cfg: EdgeDetectionConfig = settings.edge_detection

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
        self.target_size = tuple(map(int, size_str.split(",")))

        if not os.path.exists(self.image_path):
            raise FileNotFoundError(f"Test image not found: {self.image_path}")

        self.image_data = preprocess_image(self.image_path, self.target_size)
        self.padded_shape = self.image_data["rgb"]["padded"].shape[:2]

    def test_direct_detect_structure(self):
        # Direct EdgeDetector.detect returns nested cues and combined
        detector = EdgeDetector(self.edge_cfg)
        result = detector.detect(self.image_data)

        # Must have 'cues' and 'combined'
        self.assertIn("cues", result)
        self.assertIn("combined", result)

        # 'cues' should only contain the 'canny' block when configured
        # Here we only test that the configured methods are present
        expected_methods = set(self.edge_cfg.methods)
        self.assertEqual(set(result["cues"].keys()), expected_methods)

        for method in expected_methods:
            block = result["cues"][method]
            for sub in ["map", "density", "salience"]:
                self.assertIn(sub, block)
                arr = block[sub]
                self.assertIsInstance(arr, np.ndarray)
                self.assertEqual(arr.shape, self.padded_shape)

        # 'combined' must have strength, density, salience
        combined = result["combined"]
        for sub in ["strength", "density", "salience"]:
            self.assertIn(sub, combined)
            arr = combined[sub]
            self.assertIsInstance(arr, np.ndarray)
            self.assertEqual(arr.shape, self.padded_shape)

    def test_invalid_method_raises(self):
        bad_cfg = self.edge_cfg.model_copy(update={"methods": ["invalid"]})
        with self.assertRaises(ValueError):
            EdgeDetector(bad_cfg).detect(self.image_data)

    def test_feature_extractor_flattened_schema(self):
        fe = FeatureExtractor(
            enable_color=False,
            enable_edges=True,
            enable_objects=False,
            enable_saliency=False,
            use_dl_models=False,
            color_detector_config=self.color_cfg,
            edge_detector_config=self.edge_cfg
        )
        features = fe.extract(self.image_data)

        self.assertIn("edges", features)
        edges = features["edges"]
        self.assertIsInstance(edges, dict)

        # Placeholders
        self.assertIn("detections", edges)
        self.assertIn("segmentation", edges)
        self.assertIsNone(edges["detections"])
        self.assertIsNone(edges["segmentation"])

        # Check per-cue blocks
        for method in self.edge_cfg.methods:
            block = edges[method]
            for sub in ["map", "density", "salience"]:
                self.assertIn(sub, block)
                arr = block[sub]
                self.assertIsInstance(arr, np.ndarray)
                self.assertEqual(arr.shape, self.padded_shape)

        # Check combined fields at top-level
        for sub in ["strength", "density", "salience"]:
            self.assertIn(sub, edges)
            arr = edges[sub]
            self.assertIsInstance(arr, np.ndarray)
            self.assertEqual(arr.shape, self.padded_shape)
            self.assertTrue((arr >= 0).all(), f"{sub} contains negative values")

    def test_density_reasonable(self):
        fe = FeatureExtractor(
            enable_color=False,
            enable_edges=True,
            enable_objects=False,
            enable_saliency=False,
            use_dl_models=False,
            color_detector_config=self.color_cfg,
            edge_detector_config=self.edge_cfg
        )
        features = fe.extract(self.image_data)
        edges = features["edges"]

        # Validate sparsity/density of raw edge maps
        for method in self.edge_cfg.methods:
            block = edges[method]
            m = block["map"]
            ratio = np.count_nonzero(m) / m.size
            self.assertGreater(ratio, 0.001, f"{method} edge map too sparse.")
            if method in {"sobel", "laplacian"}:
                self.assertLess(ratio, 0.9, f"{method} edge map too dense.")
            else:
                self.assertLess(ratio, 0.5, f"{method} edge map too dense.")


if __name__ == "__main__":
    unittest.main()