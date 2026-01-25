import os
import unittest
import numpy as np
from src.analyzer.preprocessing import preprocess_image


class TestImagePreprocessing(unittest.TestCase):
    def setUp(self):
        # Determine test image path
        env_path = os.getenv("IMAGE_PATH")
        if env_path and os.path.exists(env_path):
            self.image_path = env_path
        else:
            # fallback to first image in benchmarking/image_set
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "benchmarking", "image_set"))
            images = [f for f in os.listdir(base_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
            if images:
                self.image_path = os.path.join(base_dir, images[0])
            else:
                # ultimate fallback
                PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                self.image_path = os.path.join(PROJECT_ROOT, "analysis", "image_set", "poppies.jpeg")

        # Determine target size
        size_str = os.getenv("TARGET_SIZE", "224,224")
        width, height = map(int, size_str.split(","))
        self.target_size = (width, height)

        # Run preprocessing
        self.output = preprocess_image(self.image_path, self.target_size)

    def test_top_level_keys(self):
        expected_keys = {"exif", "original_aspect_ratio", "padding", "rgb", "bgr", "gray", "hsv", "lab"}
        self.assertTrue(expected_keys.issubset(set(self.output.keys())))

    def test_subkeys_per_space(self):
        for space in ["rgb", "bgr", "gray", "hsv", "lab"]:
            self.assertIn("og", self.output[space])
            self.assertIn("og_normalized", self.output[space])
            self.assertIn("padded", self.output[space])
            self.assertIn("padded_normalized", self.output[space])

    def test_image_shapes_match(self):
        w, h = self.target_size
        for space in ["rgb", "bgr", "hsv", "lab"]:
            self.assertEqual(self.output[space]["padded"].shape, (h, w, 3))
            self.assertEqual(self.output[space]["padded_normalized"].shape, (h, w, 3))
        self.assertEqual(self.output["gray"]["padded"].shape, (h, w))
        self.assertEqual(self.output["gray"]["padded_normalized"].shape, (h, w))

    def test_normalization_bounds(self):
        for space in ["rgb", "bgr", "gray", "hsv"]:
            padded_norm = self.output[space]["padded_normalized"]
            self.assertTrue(
                np.all((padded_norm >= 0) & (padded_norm <= 1)),
                msg=f"{space} normalized values out of bounds."
            )

        lab_norm = self.output["lab"]["padded_normalized"]
        l, a, b = lab_norm[..., 0], lab_norm[..., 1], lab_norm[..., 2]
        self.assertTrue(np.all((l >= 0) & (l <= 1)), msg="LAB L channel out of [0,1] range.")
        self.assertTrue(np.all((a >= -1) & (a <= 1)), msg="LAB a* channel out of [-1,1] range.")
        self.assertTrue(np.all((b >= -1) & (b <= 1)), msg="LAB b* channel out of [-1,1] range.")

    def test_padding_structure(self):
        pad = self.output["padding"]
        self.assertIn(abs(pad["top"] - pad["bottom"]), [0, 1])
        self.assertIn(abs(pad["left"] - pad["right"]), [0, 1])

    def test_exif_is_dict(self):
        self.assertIsInstance(self.output["exif"], dict)

    def test_aspect_ratio(self):
        self.assertGreater(self.output["original_aspect_ratio"], 0)

    def test_original_shape_consistency(self):
        for space in ["rgb", "bgr", "gray", "hsv", "lab"]:
            original = self.output[space]["og"]
            normalized = self.output[space]["og_normalized"]
            self.assertEqual(original.shape, normalized.shape)

    def test_padded_shape_consistency(self):
        for space in ["rgb", "bgr", "gray", "hsv", "lab"]:
            padded = self.output[space]["padded"]
            normalized = self.output[space]["padded_normalized"]
            self.assertEqual(padded.shape, normalized.shape)

    def test_exif_keys_presence(self):
        exif = self.output.get("exif", {})
        self.assertIsInstance(exif, dict)


if __name__ == "__main__":
    unittest.main()