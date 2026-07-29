import os
import cv2
import torch
import torchvision.transforms as transforms
from PIL import Image
import torchvision.models as models

# ==================== 全局变量（模块级单例） ====================
# 这样确保 ResNet 只在第一次被调用时加载，后续调用直接复用
_resnet = None
_device = None

def get_resnet(device='cpu'):
    """懒加载 ResNet18（只在第一次调用时加载）"""
    global _resnet, _device
    if _resnet is None:
        _device = device
        resnet = models.resnet18(weights='DEFAULT')
        resnet = torch.nn.Sequential(*list(resnet.children())[:-1])
        resnet.to(device)
        resnet.eval()
        _resnet = resnet
        print("✅ ResNet18 特征提取器已加载（懒加载）")
    return _resnet

def extract_features_from_image(image_path, device='cpu'):
    """
    输入一张图片路径，输出 512 维特征向量（numpy 数组）
    这个函数可以被任何脚本复用
    """
    # 1. 读取图片
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"无法读取图片：{image_path}")
    
    # 2. 预处理
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, (224, 224))
    
    # 3. 转 Tensor
    pil_img = Image.fromarray(img_resized)
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    img_tensor = transform(pil_img).unsqueeze(0).to(device)
    
    # 4. 提取特征
    model = get_resnet(device)
    with torch.no_grad():
        features = model(img_tensor).squeeze().cpu().numpy()
    
    return features