import unittest
from src.feature_extraction import extract_features

class TestFeatureExtraction(unittest.TestCase):

    def test_extract_features_valid_image(self):
        # 测试有效图像的特征提取
        image_path = 'data/raw/sample_face.jpg'  # 替换为有效的图像路径
        features = extract_features(image_path)
        self.assertIsNotNone(features)
        self.assertGreater(len(features), 0)

    def test_extract_features_invalid_image(self):
        # 测试无效图像的特征提取
        image_path = 'data/raw/invalid_image.jpg'  # 替换为无效的图像路径
        with self.assertRaises(ValueError):
            extract_features(image_path)

    def test_extract_features_empty_image(self):
        # 测试空图像的特征提取
        image_path = 'data/raw/empty_image.jpg'  # 替换为空图像路径
        with self.assertRaises(ValueError):
            extract_features(image_path)

if __name__ == '__main__':
    unittest.main()