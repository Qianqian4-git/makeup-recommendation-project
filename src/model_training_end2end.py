import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, models
from PIL import Image
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
from config import TARGET_ATTRS

load_dotenv()

# ==================== 配置 ====================
IMG_DIR = os.getenv("RAW_DATA_DIR")
PROCESSED_DIR = os.getenv("PROCESSED_DATA_DIR")
DEVICE = os.getenv("DEVICE", "cpu")
BATCH_SIZE = 64
EPOCHS = 20
LEARNING_RATE = 0.0001

# ==================== 1. 自定义数据集 ====================
class CelebAAttributeDataset(Dataset):
    def __init__(self, img_dir, df, attr_df, transform=None):
        self.img_dir = img_dir
        self.df = df  # 直接接收 DataFrame，不再读文件
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
        
        # 获取标签
        labels = self.attr_df[self.attr_df['filename'] == img_name][TARGET_ATTRS].values[0]
        labels = (labels == 1).astype(np.float32)
        
        return image, torch.tensor(labels, dtype=torch.float32)

# ==================== 2. 加载属性文件 ====================
attr_file = os.getenv("ATTR_FILE")
if not attr_file:
    raise ValueError("请在 .env 中设置 ATTR_FILE")

attr_df = pd.read_csv(attr_file, sep=r'\s+', skiprows=2, header=None)
with open(attr_file, 'r') as f:
    lines = f.readlines()
header_line = lines[1].strip().split()
attr_names = ['filename'] + header_line
attr_df.columns = attr_names

# 只取训练集
train_csv = os.path.join(PROCESSED_DIR, "train_images.csv")
train_df = pd.read_csv(train_csv)
train_filenames = train_df['filename'].tolist()
attr_df_train = attr_df[attr_df['filename'].isin(train_filenames)]

# ==================== 3. 划分训练/验证 ====================
# 快速测试：先用 5000 张，正式跑请注释掉下面这行
#train_df_sub = train_df.head(5000)
#attr_df_train_sub = attr_df_train[attr_df_train['filename'].isin(train_df_sub['filename'].tolist())]

# 正式跑全量，注释上面两行，取消注释下面两行
train_df_sub = train_df
attr_df_train_sub = attr_df_train

train_ids, val_ids = train_test_split(train_df_sub['filename'].tolist(), test_size=0.2, random_state=42)
train_df_final = train_df_sub[train_df_sub['filename'].isin(train_ids)]
val_df_final = train_df_sub[train_df_sub['filename'].isin(val_ids)]

print(f"训练集图片数: {len(train_df_final)}, 验证集图片数: {len(val_df_final)}")

# ==================== 4. 数据增强与加载器 ====================
transform_train = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
transform_val = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

train_dataset = CelebAAttributeDataset(IMG_DIR, train_df_final, attr_df_train_sub, transform=transform_train)
val_dataset = CelebAAttributeDataset(IMG_DIR, val_df_final, attr_df_train_sub, transform=transform_val)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

# ==================== 5. 模型 ====================
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

model = EndToEndModel().to(DEVICE)
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# ==================== 6. 训练 ====================
print("🚀 开始端到端训练...")
best_val_loss = float('inf')
for epoch in range(EPOCHS):
    model.train()
    train_loss = 0.0
    for images, labels in train_loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
    
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            outputs = model(images)
            loss = criterion(outputs, labels)
            val_loss += loss.item()
    
    avg_train_loss = train_loss / len(train_loader)
    avg_val_loss = val_loss / len(val_loader)
    print(f"Epoch {epoch+1}/{EPOCHS} | Train Loss: {avg_train_loss:.4f} | Val Loss: {avg_val_loss:.4f}")
    
    if avg_val_loss < best_val_loss:
        best_val_loss = avg_val_loss
        torch.save(model.state_dict(), "./models/best_model_end2end.pth")
        print("   ✅ 保存最佳模型 (Val Loss: {:.4f})".format(best_val_loss))

print("🎉 训练完成！")