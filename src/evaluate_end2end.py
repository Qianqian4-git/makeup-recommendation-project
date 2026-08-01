import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, models
from PIL import Image
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from dotenv import load_dotenv
from config import TARGET_ATTRS

load_dotenv()

# ==================== 配置 ====================
IMG_DIR = os.getenv("RAW_DATA_DIR")
PROCESSED_DIR = os.getenv("PROCESSED_DATA_DIR")
DEVICE = os.getenv("DEVICE", "cpu")
BATCH_SIZE = 64

# ==================== 1. 定义模型结构（必须和训练时一模一样） ====================
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

# ==================== 2. 加载模型权重 ====================
model_path = "./models/best_model_end2end.pth"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"模型文件不存在：{model_path}")

model = EndToEndModel().to(DEVICE)
model.load_state_dict(torch.load(model_path, map_location=DEVICE))
model.eval()
print("✅ 模型加载成功！")

# ==================== 3. 加载测试集图片和标签 ====================
# 加载测试集 CSV
test_csv = os.path.join(PROCESSED_DIR, "test_images.csv")
test_df = pd.read_csv(test_csv)

# 【快速验证】只取前 2000 张，正式评估全量时注释掉下一行
test_df = test_df.head(2000)
print(f"测试集样本数: {len(test_df)}")

# 加载属性文件（获取真实标签）
attr_file = os.getenv("ATTR_FILE")
attr_df = pd.read_csv(attr_file, sep=r'\s+', skiprows=2, header=None)
with open(attr_file, 'r') as f:
    lines = f.readlines()
header_line = lines[1].strip().split()
attr_names = ['filename'] + header_line
attr_df.columns = attr_names

# 筛选出测试集的标签
attr_df_test = attr_df[attr_df['filename'].isin(test_df['filename'].tolist())]
print(f"匹配到的测试集标签数: {len(attr_df_test)}")

# ==================== 4. 数据预处理 ====================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# ==================== 5. 自定义测试数据集（不包含增强） ====================
class TestDataset(Dataset):
    def __init__(self, img_dir, df, attr_df, transform=None):
        self.img_dir = img_dir
        self.df = df
        self.attr_df = attr_df
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img_name = row['filename']
        img_path = os.path.join(self.img_dir, img_name)
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        
        # 获取真实标签
        labels = self.attr_df[self.attr_df['filename'] == img_name][TARGET_ATTRS].values[0]
        labels = (labels == 1).astype(np.float32)
        return image, torch.tensor(labels, dtype=torch.float32)

# ==================== 6. 创建 DataLoader 并推理 ====================
test_dataset = TestDataset(IMG_DIR, test_df, attr_df_test, transform=transform)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

all_preds = []
all_labels = []

with torch.no_grad():
    for images, labels in test_loader:
        images = images.to(DEVICE)
        outputs = model(images)
        probs = torch.sigmoid(outputs).cpu().numpy()
        preds = (probs > 0.5).astype(int)
        all_preds.append(preds)
        all_labels.append(labels.numpy())

y_pred = np.vstack(all_preds)
y_true = np.vstack(all_labels)

# ==================== 7. 计算评估指标 ====================
print("\n" + "=" * 60)
print("📊 端到端模型测试集评估结果")
print("=" * 60)

print(f"{'属性':<20} {'准确率':<8} {'召回率':<8} {'F1':<8}")
print("-" * 50)

macro_recall = 0
macro_f1 = 0

for i, attr in enumerate(TARGET_ATTRS):
    acc = accuracy_score(y_true[:, i], y_pred[:, i])
    rec = recall_score(y_true[:, i], y_pred[:, i], zero_division=0)
    f1 = f1_score(y_true[:, i], y_pred[:, i], zero_division=0)
    macro_recall += rec
    macro_f1 += f1
    print(f"{attr:<20} {acc:.4f}    {rec:.4f}    {f1:.4f}")

macro_recall /= len(TARGET_ATTRS)
macro_f1 /= len(TARGET_ATTRS)

print("-" * 50)
print(f"{'宏平均 (Macro)':<20} {'':<8} {macro_recall:.4f}    {macro_f1:.4f}")
print("=" * 60)