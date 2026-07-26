import unittest
import pandas as pd
from src.data_cleaning import clean_data

class TestDataCleaning(unittest.TestCase):

    def setUp(self):
        # 创建一个示例数据框用于测试
        self.raw_data = pd.DataFrame({
            'image_path': ['path/to/image1.jpg', 'path/to/image2.jpg'],
            'label': ['round', 'oval'],
            'other_info': ['info1', 'info2']
        })

    def test_clean_data(self):
        # 测试数据清洗功能
        cleaned_data = clean_data(self.raw_data)
        
        # 检查清洗后的数据是否符合预期
        self.assertEqual(len(cleaned_data), 2)
        self.assertIn('image_path', cleaned_data.columns)
        self.assertIn('label', cleaned_data.columns)
        self.assertNotIn('other_info', cleaned_data.columns)

    def test_empty_data(self):
        # 测试空数据的处理
        empty_data = pd.DataFrame(columns=['image_path', 'label', 'other_info'])
        cleaned_data = clean_data(empty_data)
        
        # 检查清洗后的数据是否为空
        self.assertTrue(cleaned_data.empty)

if __name__ == '__main__':
    unittest.main()