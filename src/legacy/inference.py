# ============================================================
# DEPRECATED (弃用)
# 功能: 加载旧版分类器进行推理（基于冻结特征）
# 替代方案: 改用 inference_end2end.py（端到端推理）
# 弃用原因: 对应的旧模型（best_model.pth）已不再使用，
#           新模型性能更好且无需单独提取特征文件
# 归档日期: 2026-08-02
# ============================================================


import os
import sys
from pathlib import Path

# ===== 把项目根目录加到 Python 路径 =====
root_dir = Path(__file__).parent.parent  # inference.py 在 src/ 下，parent 就是 src/，再 parent 就是根目录
sys.path.insert(0, str(root_dir))

import numpy as np
import torch
from dotenv import load_dotenv

from src.config import TARGET_ATTRS
from src.utils.feature_utils import extract_features_from_image
from src.models import FaceAttributeModel
from src.recommendation_engine import recommend_makeup
from src.config import TARGET_ATTRS

# 预测阈值：高于此值判定属性存在
PREDICTION_THRESHOLD = 0.35  # 建议 0.35 作为中间值

load_dotenv()
MODEL_SAVE_PATH = os.getenv("MODEL_SAVE_PATH","./models/best_model.pth")
DEVICE = os.getenv("DEVICE","cpu")

#加载模型
attr_model = FaceAttributeModel().to(DEVICE)
attr_model.load_state_dict(torch.load(MODEL_SAVE_PATH, map_location=DEVICE))
attr_model.to(DEVICE)
attr_model.eval()
print("✅ 推理模型加载完成！")


#推理函数
def predict(image_path, gender=None):
    # 1. 提取特征 (512维)
    features = extract_features_from_image(image_path, device=DEVICE)

    # 2. 如果未指定性别，先自动预测性别
    if gender is None:
        # 临时用0占位，但要确保是二维 (1, 513)
        X_temp = np.hstack([features, [0]]).reshape(1, -1)
        X_tensor = torch.tensor(X_temp, dtype=torch.float32).to(DEVICE)
        with torch.no_grad():
            logits = attr_model(X_tensor)
            probs_temp = torch.sigmoid(logits).cpu().numpy().flatten()
        gender = 1 if probs_temp[0] > 0.5 else 0

    # 3. 用确定后的性别构建最终输入 (二维)
    X = np.hstack([features, [gender]]).reshape(1, -1)
    X_tensor = torch.tensor(X, dtype=torch.float32).to(DEVICE)
    with torch.no_grad():
        logits = attr_model(X_tensor)
        probs = torch.sigmoid(logits).cpu().numpy().flatten()

    # 4. 转为0/1标签并调用推荐规则
    predicted_attrs = (probs > PREDICTION_THRESHOLD).astype(int)
    makeup_name, reason = recommend_makeup(predicted_attrs)

    return {
        'attributes': dict(zip(TARGET_ATTRS, probs.tolist())),
        'makeup': makeup_name,
        'reason': reason
    }
if __name__ == "__main__":
    test_image = "./data/raw/ai.jpg"  # 改成你的图片路径
    if os.path.exists(test_image):
        result = predict(test_image,gender=0)
        print("=" * 50)
        print("💄 妆容推荐结果")
        print("=" * 50)
        for attr, prob in result['attributes'].items():
            if prob > 0.3:
                print(f"  {attr}: {prob:.2%}")
        print(f"\n✨ 推荐妆容：{result['makeup']}")
        print(f"📝 理由：{result['reason']}")
    else:
        print(f"⚠️ 测试图片不存在：{test_image}")