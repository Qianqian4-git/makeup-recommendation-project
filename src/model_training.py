import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

def train_model(features, labels):
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

    # 初始化模型
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # 训练模型
    model.fit(X_train, y_train)

    # 预测测试集
    predictions = model.predict(X_test)

    # 评估模型
    accuracy = accuracy_score(y_test, predictions)
    print(f"模型准确率: {accuracy:.2f}")

    return model

if __name__ == "__main__":
    # 假设特征和标签已经准备好
    features = pd.read_csv('data/processed/features.csv')  # 处理后的特征数据
    labels = pd.read_csv('data/processed/labels.csv')      # 处理后的标签数据

    # 训练模型
    model = train_model(features, labels)

    # 保存模型
    joblib.dump(model, 'model/makeup_recommendation_model.pkl')