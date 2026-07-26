import unittest
from src.model_training import train_model, evaluate_model

class TestModelTraining(unittest.TestCase):

    def setUp(self):
        # 在这里设置测试所需的初始数据
        self.features = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        self.labels = [0, 1]

    def test_train_model(self):
        # 测试模型训练功能
        model = train_model(self.features, self.labels)
        self.assertIsNotNone(model, "模型训练失败，返回的模型为 None")

    def test_evaluate_model(self):
        # 测试模型评估功能
        model = train_model(self.features, self.labels)
        accuracy = evaluate_model(model, self.features, self.labels)
        self.assertGreaterEqual(accuracy, 0, "模型准确率应大于等于 0")

if __name__ == '__main__':
    unittest.main()