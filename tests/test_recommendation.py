import unittest
from src.recommendation import recommend_makeup

class TestMakeupRecommendation(unittest.TestCase):

    def setUp(self):
        # 在每个测试之前设置测试数据
        self.test_image = "path/to/test/image.jpg"  # 替换为测试图像的路径
        self.expected_recommendations = ["自然妆", "晚宴妆"]  # 替换为预期的推荐妆容

    def test_recommend_makeup(self):
        # 测试推荐妆容的功能
        recommendations = recommend_makeup(self.test_image)
        self.assertIn("自然妆", recommendations)
        self.assertIn("晚宴妆", recommendations)

    def test_empty_image(self):
        # 测试空图像输入的处理
        with self.assertRaises(ValueError):
            recommend_makeup("")

    def test_invalid_image_format(self):
        # 测试无效图像格式的处理
        with self.assertRaises(ValueError):
            recommend_makeup("path/to/invalid/image.txt")

if __name__ == '__main__':
    unittest.main()