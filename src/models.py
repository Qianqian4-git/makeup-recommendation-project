import torch
import torch.nn as nn

# ==================== 定义神经网络结构 ====================
class FaceAttributeModel(nn.Module):
    def __init__(self, input_dim, hidden_dims, output_dim):
        super(FaceAttributeModel, self).__init__()
        layers = []
        prev_dim = input_dim
        for h_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, h_dim))
            layers.append(nn.BatchNorm1d(h_dim))
            layers.append(nn.ReLU())
            #把它提到 0.3，让它学习时更“艰难”，从而学会用更多特征共同决策。
            layers.append(nn.Dropout(0.3)) #之前是 Dropout(0.2)，意思是随机丢弃 20% 的神经元。
            prev_dim = h_dim
        layers.append(nn.Linear(prev_dim, output_dim))
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x)