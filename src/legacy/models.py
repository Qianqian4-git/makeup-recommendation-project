# ============================================================
# DEPRECATED (弃用)
# 功能: 定义旧版全连接分类器 FaceAttributeModel
#       输入: 513 维特征 (512 视觉特征 + 性别)
#       输出: 14 个面部属性 (0/1)
# 替代方案: 请使用端到端方案中的 EndToEndModel
#           (定义在 model_training_end2end.py / inference_end2end.py)
# 弃用原因: 
#   1. 该模型依赖冻结特征 (ResNet/FaceNet)，实验证明预训练特征
#      对 CelebA 属性（如脸型、厚唇）区分度不足，宏平均 F1 仅 0.12
#   2. 端到端方案 (ResNet18 + 自定义全连接层) 可直接从原始图片学习，
#      宏平均 F1 提升至 0.52+，验证 Loss 降至 0.2786
# 归档日期: 2026-08-02
# ============================================================


import torch
import torch.nn as nn
from src.config import INPUT_DIM, HIDDEN_DIMS, OUTPUT_DIM
# ==================== 定义神经网络结构 ====================
class FaceAttributeModel(nn.Module):
    def __init__(self):
        super().__init__()
        layers = []
        prev_dim = INPUT_DIM
        for h_dim in HIDDEN_DIMS:
            layers.append(nn.Linear(prev_dim, h_dim))
            layers.append(nn.BatchNorm1d(h_dim))
            layers.append(nn.ReLU())
            #把它提到 0.3，让它学习时更“艰难”，从而学会用更多特征共同决策。
            layers.append(nn.Dropout(0.3)) #之前是 Dropout(0.2)，意思是随机丢弃 20% 的神经元。
            prev_dim = h_dim
        layers.append(nn.Linear(prev_dim, OUTPUT_DIM))
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x)