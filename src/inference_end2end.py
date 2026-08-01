import sys
import os
# 将项目根目录加入 sys.path（使 from src.xxx 能正常工作）
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
from dotenv import load_dotenv

# 现在可以正常导入 src 下的模块
from src.config import TARGET_ATTRS
from src.recommendation_engine import recommend_makeup

load_dotenv()

# ==================== 1. 定义模型结构（和训练时一致） ====================
class EndToEndModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.backbone = models.resnet18(weights='DEFAULT')
        num_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Sequential(
            nn.Linear(num_features, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, len(TARGET_ATTRS))
        )

    def forward(self, x):
        return self.backbone(x)

# ==================== 2. 加载模型 ====================
DEVICE = "cpu"
model_path = "./models/best_model_end2end.pth"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"模型文件不存在: {model_path}")

model = EndToEndModel().to(DEVICE)
model.load_state_dict(torch.load(model_path, map_location=DEVICE))
model.eval()
print("✅ 端到端模型加载成功！")

# ==================== 3. 图片预处理 ====================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def predict_image(image_path):
    """输入图片路径，返回妆容推荐结果"""
    # 读取图片
    image = Image.open(image_path).convert('RGB')
    input_tensor = transform(image).unsqueeze(0).to(DEVICE)
    
    # 推理
    with torch.no_grad():
        outputs = model(input_tensor)
        probs = torch.sigmoid(outputs).cpu().numpy().flatten()
        preds = (probs > 0.4).astype(int)
    
    # 调用推荐引擎
    makeup, reason = recommend_makeup(preds)
    
    # 打印检测到的属性（概率 > 0.5）
    print("\n🔍 模型检测到的属性:")
    for attr, prob in zip(TARGET_ATTRS, probs):
        if prob > 0.4:
            print(f"  {attr}: {prob:.2%}")
    
    return makeup, reason

# ==================== 4. 测试入口 ====================
if __name__ == "__main__":
    import glob
    # 自动从 data/raw/ 取第一张图片
    raw_dir = "./data/raw"
    image_files = glob.glob(os.path.join(raw_dir, "*.jpg")) + \
                  glob.glob(os.path.join(raw_dir, "*.png")) + \
                  glob.glob(os.path.join(raw_dir, "*.jpeg"))
    
    if image_files:
        test_image = image_files[0]
        print(f"📸 测试图片: {test_image}")
        makeup, reason = predict_image(test_image)
        print("\n" + "=" * 50)
        print(f"💄 推荐妆容: {makeup}")
        print(f"📝 推荐理由: {reason}")
        print("=" * 50)
    else:
        print("⚠️ 请在 data/raw/ 目录下放一张自拍照 (jpg/png)")