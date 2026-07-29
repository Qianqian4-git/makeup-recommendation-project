import os
import numpy as np
import torch
from dotenv import load_dotenv
from config import TARGET_ATTRS
from utils.feature_utils import extract_features_from_image
from models import FaceAttributeModel
from recommendation_engine import recommend_makeup, ATTR_NAMES

load_dotenv()
MODEL_SAVE_PATH = os,getenv("MODEL_SAVE_PATH","./models/best_model.pth")
DEVICE = os.getenv("DEVICE","cpu")

#加载模型
attr_model = FaceAttributeModel().to(DEVICE)
attr_model.load_state_dict(torch.load(MODEL_SAVE_PATH, map_location=DEVICE))
attr_model.to(DEVICE)
attr_model.eval()
print("✅ 推理模型加载完成！")


#推理函数
def predict(image_path,gender):
    """
    完整推理流程：图片 → 特征 → 属性预测 → 妆容推荐
    """
    # 1. 提取特征
    features = extract_features_from_image(image_path, device=DEVICE)
    
    # 2. 拼接性别
    X = np.hstack([features,[gender]]).reshape(1,-1)
    X_tensor = torch.tensor(X,dtype = torch.float32).to(DEVICE)

    # 3. 属性预测
    with torch.no_grad():
        logits = attr_model(X_tensor)
        probs = torch.sigmoid(attr_logits).cpu().numpy().flatten()
    
    # 4.调用推荐引擎
    makeup_name,reason = recommend_makeup(probs)
    return {
        'attributes':dict(zip(ATTR_NAMES,probs.tolist())),
        'makeup':makeup_name,
        'reason':reason
    }


if __name__ == "__main__":
    test_image = "E:/test_selfie.jpg"  # 改成你的图片路径
    if os.path.exists(test_image):
        result = predict(test_image)
        print("=" * 50)
        print("💄 妆容推荐结果")
        print("=" * 50)
        for attr, prob in result['attributes'].items():
            if prob > 0.5:
                print(f"  {attr}: {prob:.2%}")
        print(f"\n✨ 推荐妆容：{result['makeup']}")
        print(f"📝 理由：{result['reason']}")
    else:
        print(f"⚠️ 测试图片不存在：{test_image}")