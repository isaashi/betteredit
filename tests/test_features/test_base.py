import os
import unittest
import numpy as np

from src.betteredit.config import Settings
from src.analyzer.features.base import FeatureExtractor
from src.analyzer.preprocessing import preprocess_image


class TestFeatureExtractor(unittest.TestCase):

    def setUp(self):
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
        width, height = map(int, size_str.split(","))
        self.target_size = (width, height)

        # Preprocess image
        self.image_data = preprocess_image(self.image_path, self.target_size)

        # Load and validate config
        self.cfg = Settings.load()

    def test_extract_with_edges(self):
        # Enable only edge detection
        fe = FeatureExtractor(
            enable_color=False,
            enable_edges=True,
            enable_objects=False,
            enable_saliency=False,
            use_dl_models=False,
            color_detector_config=self.cfg.color_detection,
            edge_detector_config=self.cfg.edge_detection
        )
        features = fe.extract(self.image_data)

        # 'edges' section present and is a dict
        self.assertIn('edges', features)
        edges = features['edges']
        self.assertIsInstance(edges, dict)

        # Placeholders should exist
        self.assertIn('detections', edges)
        self.assertIn('segmentation', edges)
        self.assertIsNone(edges['detections'])
        self.assertIsNone(edges['segmentation'])

        # Validate per-method cue blocks
        methods = ['canny', 'sobel', 'piotr', 'laplacian']
        for method in methods:
            self.assertIn(method, edges)
            block = edges[method]
            self.assertIsInstance(block, dict)
            for sub in ['map', 'density', 'salience']:
                self.assertIn(sub, block)
                arr = block[sub]
                self.assertIsInstance(arr, np.ndarray)

        # Validate combined fused outputs
        for sub in ['strength', 'density', 'salience']:
            self.assertIn(sub, edges)
            arr = edges[sub]
            self.assertIsInstance(arr, np.ndarray)

    def test_extract_with_color(self):
        # Enable only color detection
        fe = FeatureExtractor(
            enable_color=True,
            enable_edges=False,
            enable_objects=False,
            enable_saliency=False,
            use_dl_models=False,
            color_detector_config=self.cfg.color_detection,
            edge_detector_config=self.cfg.edge_detection
        )
        features = fe.extract(self.image_data)

        # 'color' section present and is a dict
        self.assertIn('color', features)
        color = features['color']
        self.assertIsInstance(color, dict)

        # Placeholders should exist
        self.assertIn('detections', color)
        self.assertIn('segmentation', color)
        self.assertIsNone(color['detections'])
        self.assertIsNone(color['segmentation'])

        # Validate per-cue blocks
        cues = [
            'hue', 'saturation', 'luminance', 'rarity',
            'hue_contrast', 'luminance_contrast'
        ]
        for cue in cues:
            self.assertIn(cue, color)
            block = color[cue]
            self.assertIsInstance(block, dict)
            for sub in ['map', 'density', 'salience']:
                self.assertIn(sub, block)
                arr = block[sub]
                self.assertIsInstance(arr, np.ndarray)

        # Validate combined fused outputs
        for sub in ['strength', 'density', 'salience']:
            self.assertIn(sub, color)
            arr = color[sub]
            self.assertIsInstance(arr, np.ndarray)

    def test_disabled_features(self):
        # All features disabled
        fe = FeatureExtractor(
            enable_color=False,
            enable_edges=False,
            enable_objects=False,
            enable_saliency=False,
            use_dl_models=False,
            color_detector_config=self.cfg.color_detection,
            edge_detector_config=self.cfg.edge_detection
        )
        features = fe.extract(self.image_data)
        self.assertEqual(features, {})


if __name__ == '__main__':
    unittest.main()