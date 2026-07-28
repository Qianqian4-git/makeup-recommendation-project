import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from dotenv import load_dotenv
from models import FaceAttributeModel

load_dotenv()

# ==================== 1. 配置 ====================
attr_file = os.getenv("ATTR_FILE")
FEATURES_PATH = os.getenv("FEATURES_SAVE_PATH", "./data/processed/celeba_features.npz")
MODEL_SAVE_PATH = os.getenv("MODEL_SAVE_PATH", "./models/best_model.pth")
DEVICE = os.getenv("DEVICE", "cpu")
EPOCHS = 60
BATCH_SIZE = 64
LEARNING_RATE = 0.0005 #0.001 对于这个小网络来说太快了，它很容易跳过最优点。改成 0.0005

os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)

print("="*60)
print("💄 训练面部属性分析模型（14个核心属性）")
print("="*60)

# ==================== 2. 定义核心属性（14个） ====================
TARGET_ATTRS = [
    'Male',              # 性别（-1男，1女）
    'Oval_Face',         # 椭圆脸/鹅蛋脸
    'Chubby',            # 圆胖脸
    'High_Cheekbones',   # 高颧骨
    'Double_Chin',       # 双下巴
    'Narrow_Eyes',       # 细长眼/丹凤眼
    'Arched_Eyebrows',   # 弯眉
    'Bushy_Eyebrows',    # 浓眉
    'Big_Nose',          # 大鼻子
    'Pointy_Nose',       # 尖鼻子
    'Big_Lips',          # 厚嘴唇
    'Mouth_Slightly_Open', # 微张嘴（影响唇妆推荐）
    'Pale_Skin',         # 苍白皮肤/冷白皮
    'Young'              # 年轻态
]
NUM_ATTRS = len(TARGET_ATTRS)
print(f" 目标属性: {TARGET_ATTRS}")

# ==================== 3. 加载数据 ====================
print("\n 加载特征和属性标签...")

# 3.1 加载特征文件（.npz 格式）
data = np.load(FEATURES_PATH)
features = data['features']          # (N, 512)
genders = data['gender']             # (N,)
print(f"✅ 特征加载完成: {features.shape}")
print(f"✅ 性别标签加载完成: {genders.shape}")

# 3.2 加载属性标签

if not os.path.exists(attr_file):
    raise FileNotFoundError(f"属性文件 {attr_file} 不存在，请检查路径。")

# 读取属性文件第二行(注意：属性文件的第一行是样本数量，第二行是属性名称，后续每行是样本的属性值)
attr_name_df = pd.read_csv(attr_file,sep=r'\s+',skiprows=1,nrows=0)
original_cols = attr_name_df.columns.tolist()

# 过滤出目标属性
needed_indices = [0]
for attr in TARGET_ATTRS:
    if attr in original_cols:
        needed_indices.append(original_cols.index(attr))
    else:
        raise ValueError(f"属性 {attr} 在属性文件中未找到，请检查属性名称。")

# 读取文件，取需要的列
attr_df = pd.read_csv(attr_file, sep=r'\s+', skiprows=2, header=None, usecols=needed_indices)
attr_df.columns = ['filename' ] + TARGET_ATTRS

# 将属性值从 -1/1 转换为 0/1(神经网络喜欢 0/1 输入)
for attr in TARGET_ATTRS:
    attr_df[attr] = (attr_df[attr] == 1).astype(int)
print(f"属性标签加载完成：{attr_df.shape}")
print(attr_df.head(3))

# ==================== 4. 数据对齐 ====================
# 数据预处理或特征提取过程中，可能会有部分图片被过滤（如模糊图片被丢弃）
# 导致特征数据和属性数据的行数不一致。

print("\n 对齐特征和属性...")
if len(attr_df) >= len(features):
    attr_df = attr_df.iloc[:len(features)]
else:
    features = features[:len(attr_df)]

# 提取标签矩阵（N,14）
labels = attr_df[TARGET_ATTRS].values.astype(np.float32)
print(f"对齐完成，共{len(labels)}张图片，标签维度{labels.shape}")

genders = labels[:, 0]  # 性别标签



# ==================== 5. 数据集划分 ====================
# 将512维和性别拼接成513维

x = np.hstack([features,genders.reshape(-1,1)])
y = labels  # (N,14)

print(f"输出特征维度：{x.shape}")
print(f"输出标签维度：{y.shape}")

# 划分训练集和验证集
x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state=42)
print(f"训练集样本数: {len(x_train)}, 验证集样本数: {len(x_val)}")


# ==================== 6. 定义模型 ====================

model = FaceAttributeModel(
    input_dim = 513,
    # hidden_dims = [512,256,128],
    hidden_dims=[256, 128],   # 只留两层隐藏层，参数减少一半以上
    output_dim = NUM_ATTRS
).to(DEVICE)
print(f"\n模型结构:\n{model}")

# ==================== 7. 定义训练函数 ====================
# 转为 Tensor
X_train_t = torch.tensor(x_train, dtype=torch.float32)
y_train_t = torch.tensor(y_train, dtype=torch.float32)
X_val_t = torch.tensor(x_val, dtype=torch.float32)
y_val_t = torch.tensor(y_val, dtype=torch.float32)

train_dataset = TensorDataset(X_train_t, y_train_t)
val_dataset = TensorDataset(X_val_t, y_val_t)
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

criterion = nn.BCEWithLogitsLoss()  # 多标签分类专用
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# ==================== 训练（含早停） ====================
print("\n🚀 开始训练（早停 patience=10）...")
best_val_loss = float('inf')
patience_counter = 0
early_stop_patience = 10

for epoch in range(EPOCHS):
    # 训练
    model.train()
    train_loss = 0.0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
    
    # 验证
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            val_loss += loss.item()
    
    avg_train_loss = train_loss / len(train_loader)
    avg_val_loss = val_loss / len(val_loader)
    
    if (epoch + 1) % 10 == 0:
        print(f"Epoch [{epoch+1}/{EPOCHS}] Train Loss: {avg_train_loss:.4f}, Val Loss: {avg_val_loss:.4f}")
    
    # 保存最佳模型
    if avg_val_loss < best_val_loss:
        best_val_loss = avg_val_loss
        patience_counter = 0
        torch.save(model.state_dict(), MODEL_SAVE_PATH)
        print(f"Epoch [{epoch+1:2d}/{EPOCHS}] ✅ 保存最佳模型 (Val Loss: {avg_val_loss:.4f})")
    else:
        patience_counter += 1
        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch+1:2d}/{EPOCHS}] Train Loss: {avg_train_loss:.4f}, Val Loss: {avg_val_loss:.4f} (Patience: {patience_counter}/{early_stop_patience})")
    
    # 👈 优化：早停触发
    if patience_counter >= early_stop_patience:
        print(f"\n⏹️ 早停触发！验证 Loss 连续 {early_stop_patience} 轮未改善，停止训练。")
        break

print("\n🎉 训练完成！")
print(f"📁 模型已保存至: {MODEL_SAVE_PATH}")