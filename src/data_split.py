import os
import pandas as pd
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

load_dotenv()

RAW_DATA_DIR = os.getenv("RAW_DATA_DIR")
PROCESSED_DIR = os.getenv("PROCESSED_DATA_DIR")

identity_file = os.path.join(os.path.dirname(RAW_DATA_DIR), "identity_CelebA.txt")
attr_file = os.path.join(os.path.dirname(RAW_DATA_DIR), "list_attr_celeba.txt")
valid_csv = os.path.join(PROCESSED_DIR, "valid_images.csv")

# ========== 1. 读取身份文件（取前两列） ==========
identity_df = pd.read_csv(identity_file, sep=r'\s+', header=None)
identity_df = identity_df.iloc[:, :2]          # 只取前两列
identity_df.columns = ['filename', 'identity'] # 强制命名

# ========== 2. 读取属性文件（取文件名 + 性别列） ==========
attr_df = pd.read_csv(attr_file, sep=r'\s+', skiprows=2, header=None)
attr_df = attr_df.iloc[:, [0, 21]]             # 第0列文件名，第21列 Male（索引从0开始）
attr_df.columns = ['filename', 'Male']

# ========== 3. 读取清洗后的有效图片 ==========
valid_df = pd.read_csv(valid_csv)

# ========== 4. 合并（内连接） ==========
merged_df = pd.merge(identity_df, valid_df, on='filename')
merged_df = pd.merge(merged_df, attr_df, on='filename')

print(f"✅ 合并完成，共有 {len(merged_df)} 张图片")
print(f"📋 列名：{merged_df.columns.tolist()}")

# ========== 5. 按身份划分（企业级） ==========
unique_ids = merged_df['identity'].unique()
train_ids, test_ids = train_test_split(unique_ids, test_size=0.2, random_state=42)

train_df = merged_df[merged_df['identity'].isin(train_ids)]
test_df = merged_df[merged_df['identity'].isin(test_ids)]

# ========== 6. 保存 ==========
os.makedirs(PROCESSED_DIR, exist_ok=True)
train_df[['filename', 'Male']].to_csv(os.path.join(PROCESSED_DIR, "train_images.csv"), index=False)
test_df[['filename', 'Male']].to_csv(os.path.join(PROCESSED_DIR, "test_images.csv"), index=False)

print("=" * 50)
print("✅ 数据划分完成！")
print(f"📁 训练集：{os.path.join(PROCESSED_DIR, 'train_images.csv')}")
print(f"📁 测试集：{os.path.join(PROCESSED_DIR, 'test_images.csv')}")
print(f"📊 训练集图片数：{len(train_df)}")
print(f"📊 测试集图片数：{len(test_df)}")
print(f"👤 总身份人数：{len(unique_ids)}")
print("=" * 50)