# ============================================================
# DEPRECATED (弃用)
# 功能: 使用 ResNet/FaceNet 提取 512 维冻结特征
# 替代方案: 改用 model_training_end2end.py（端到端微调）
# 弃用原因: 预训练特征对 CelebA 属性（脸型/厚唇等）区分度不足，
#           冻结特征方案宏平均 F1 仅为 0.12，远低于端到端方案（0.52+）
# 归档日期: 2026-08-02
# ============================================================

import os
import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
import torchvision.models as models
from torch.utils.data import DataLoader, Dataset
from PIL import Image
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

torch_home = os.getenv("TORCH_HOME")
IMG_DIR = os.getenv("RAW_DATA_DIR")
PROCESSED_DIR = os.getenv("PROCESSED_DATA_DIR")
FEATURES_SAVE_PATH = os.getenv("FEATURES_SAVE_PATH")
TEST_FEATURES_SAVE_PATH = os.getenv("TEST_FEATURES_SAVE_PATH")#测试集
DEVICE = os.getenv("DEVICE","cpu")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 64))

# 企业级阈值：拉普拉斯方差小于此值视为模糊（数值可微调）
BLUR_THRESHOLD = 50

os.makedirs(os.path.dirname(FEATURES_SAVE_PATH), exist_ok=True)
os.makedirs(os.path.dirname(TEST_FEATURES_SAVE_PATH), exist_ok=True)

# ==================== 加载关键点（真正的万能读取法） ====================
print("📂 加载人脸关键点数据...")

# 1. 读取文件路径
landmark_file = os.getenv("LANDMARK_FILE")
if not landmark_file:
    landmark_file = os.path.join(os.path.dirname(IMG_DIR), "list_landmarks_align_celeba.txt")

landmarks_dict = {}

if os.path.exists(landmark_file):
    try:
        with open(landmark_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # ---------- 核心：自动寻找“第一行真正的数据” ----------
        def is_data_line(parts):
            """判断这一行是不是真实数据行"""
            # 1. 至少要有 文件名 + 2个坐标（最少3个元素）
            if len(parts) < 3:
                return False
            # 2. 检查后面的元素（从第2个开始）是不是纯数字（浮点数）
            #    用 try/except 看能不能转成 float
            try:
                for i in range(1, min(len(parts), 5)):  # 检查前几个坐标
                    float(parts[i])
                return True
            except ValueError:
                return False
        
        # 遍历所有行，找到第一个“数据行”的索引
        start_idx = 0
        for i, line in enumerate(lines):
            parts = line.strip().split()
            if is_data_line(parts):
                start_idx = i
                break
        
        # ---------- 从数据行开始解析 ----------
        for line in lines[start_idx:]:
            parts = line.strip().split()
            # 如果是空行或长度不够，跳过
            if len(parts) < 5:
                continue
            
            filename = parts[0]
            # 取前 4 个坐标（左眼x,y 右眼x,y）
            landmarks_dict[filename] = {
                'le_x': float(parts[1]), 'le_y': float(parts[2]),
                're_x': float(parts[3]), 're_y': float(parts[4])
            }
        
        print(f"✅ 成功加载了 {len(landmarks_dict)} 个关键点")
    
    except Exception as e:
        print(f"⚠️ 读取关键点文件失败: {e}, 将跳过人脸对齐（直接缩放）")
else:
    print("⚠️ 关键点文件不存在, 将跳过人脸对齐（直接缩放）")

# 自定义数据集类的头部
class CelebAEnterpriseDataset(Dataset):
    def __init__(self,img_dir,split_csv,transform = None):
        self.img_dir = img_dir
        self.df = pd.read_csv(split_csv)
        self.transform = transform
    
    def __len__(self):
        return len(self.df)

    #核心处理逻辑（读图 + 人脸对齐）
    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img_name = row['filename']
        gender = int(row['Male'])
        img_path = os.path.join(self.img_dir, img_name)
        img = cv2.imread(img_path)
        if img is None:
            return None
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # 人脸对齐
        if img_name in landmarks_dict:
            pts = landmarks_dict[img_name]
            left_eye = (pts['le_x'], pts['le_y'])
            right_eye = (pts['re_x'], pts['re_y'])
            dx = right_eye[0] - left_eye[0]
            dy = right_eye[1] - left_eye[1]
            angle = np.degrees(np.arctan2(dy, dx))
            eyes_center = ((left_eye[0] + right_eye[0]) // 2,
                           (left_eye[1] + right_eye[1]) // 2)
            rot_mat = cv2.getRotationMatrix2D(eyes_center, angle, scale=1.2)
            img_aligned = cv2.warpAffine(img_rgb, rot_mat, (224, 224))
        else:
            img_aligned = cv2.resize(img_rgb, (224, 224))
        
        #（模糊检测 + 转成 Tensor）
        gray = cv2.cvtColor(img_aligned, cv2.COLOR_RGB2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        if laplacian_var < BLUR_THRESHOLD:
            return None

        pil_img = Image.fromarray(img_aligned)
        if self.transform:
            pil_img = self.transform(pil_img)
        
        return pil_img, gender
    
# 过滤掉 None 的样本
def collate_fn(batch):
    batch = list(filter(lambda x: x is not None, batch))
    if len(batch) == 0:
        return torch.Tensor([]), torch.Tensor([])
    images,genders = zip(*batch)
    return torch.stack(images), torch.tensor(genders)

# 主函数 (特征提取循环 + 保存)
def extract_features():
    print("=" *50)
    print("开始特征提取...")
    print("=" *50)

     #split_csv = os.path.join(PROCESSED_DIR, "train_images.csv")
    split_csv = os.path.join(PROCESSED_DIR, "test_images.csv")
    if not os.path.exists(split_csv):
        raise FileNotFoundError(f"训练集 CSV 文件 {split_csv} 不存在，请检查路径。")
    
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
    ])

    dataset = CelebAEnterpriseDataset(IMG_DIR, split_csv, transform=transform)
    #dataset.df = dataset.df.head(1000)
    print(f"🧪 本次处理前 {len(dataset.df)} 张图片")
    
    dataloader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE, 
        shuffle=False, 
        num_workers=0,
        collate_fn=collate_fn
        )
    
    model = models.resnet18(weights='DEFAULT')
    model = torch.nn.Sequential(*(list(model.children())[:-1]))  
    model.to(DEVICE)
    model.eval()

    features_list = []
    gender_list = []

    with torch.no_grad():
        for images, genders in tqdm(dataloader, desc="提取特征"):
            if len(images) == 0:
                continue
            images = images.to(DEVICE)
            features = model(images)
            features = features.squeeze()
            features_list.append(features.cpu().numpy())
            gender_list.append(genders.numpy())

    all_features = np.vstack(features_list)
    all_genders = np.hstack(gender_list)
    np.savez(TEST_FEATURES_SAVE_PATH, features=all_features, gender=all_genders)

    print("✅ 特征提取完成！")
    print(f"📊 有效图片数：{len(all_features)}")
    print(f"📊 特征维度：{all_features.shape[1]}")


if __name__ == "__main__":
    extract_features()