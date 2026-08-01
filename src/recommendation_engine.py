import os
import numpy as np
import torch
import torch.nn as nn
from dotenv import load_dotenv

# ===== 统一从 config 读取配置 =====
from src.config import TARGET_ATTRS, INPUT_DIM, HIDDEN_DIMS, OUTPUT_DIM
from src.models import FaceAttributeModel

load_dotenv()

MODEL_SAVE_PATH = os.getenv("MODEL_SAVE_PATH", "./models/best_model.pth")
DEVICE = os.getenv("DEVICE", "cpu")

# ==================== 1. 加载模型 ====================

model = FaceAttributeModel()
model.load_state_dict(torch.load(MODEL_SAVE_PATH, map_location=DEVICE))
model.to(DEVICE)
model.eval()
print("✅ 模型加载完成！")

# ==================== 2. 妆容推荐逻辑 ====================

def recommend_makeup(attributes):
    """
    输入: 14个属性的预测值 (0或1的列表，顺序与 config.TARGET_ATTRS 一致)
    输出: 推荐妆容名称 + 推荐理由
    """
    # 解包属性（顺序与 config.TARGET_ATTRS 严格对应）
    (male, oval_face, chubby, high_cheekbones, double_chin, 
     narrow_eyes, arched_eyebrows, bushy_eyebrows, 
     big_nose, pointy_nose, big_lips, mouth_open, 
     pale_skin, young) = attributes
    
    # ---------- 逻辑 A：男性妆容推荐 ----------
    if male == 1:  
        if narrow_eyes == 1 or bushy_eyebrows == 1:
            return "韩系欧巴妆", "适合单眼皮/浓眉男生，强调清透感和干净眉形"
        elif high_cheekbones == 1 and oval_face == 0:
            return "硬朗轮廓妆", "高颧骨+非椭圆脸，适合用修容突出骨相线条"
        elif chubby == 1:
            return "自然净澈妆", "圆脸男生适合轻遮瑕+修眉，减少油腻感"
        else:
            return "职场干练妆", "标准脸型，适合哑光底妆+利落眉形，提升气质"
    
    # ---------- 逻辑 B：女性妆容推荐 ----------
    else:
        # B1: 韩系水光妆（白皮 + 鹅蛋脸 / 弯眉）
        if pale_skin == 1 and (oval_face == 1 or arched_eyebrows == 1):
            return "韩系水光妆", "冷白皮搭配鹅蛋脸/弯眉，最适合清透水光肌和咬唇妆"
        
        # B2: 日系元气妆（圆脸/高颧骨 + 年轻）
    
        elif chubby == 1 or (high_cheekbones == 1 and young == 1) :
            return "日系元气妆", "圆脸或高颧骨年轻脸型，大面积腮红可以提升面部折叠度"

        # B3: 亚裔混血妆（高颧骨 + 厚唇 / 尖鼻子）
        elif high_cheekbones == 1 and (big_lips == 1 or pointy_nose == 1):
            return "亚裔混血妆", "高颧骨配厚唇或尖鼻，适合用修容打造立体混血感"
        
        # B4: 派对浓妆（浓眉 + 厚唇 / 双下巴）
        elif bushy_eyebrows == 1 and (big_lips == 1 or double_chin == 1):
            return "派对浓妆", "浓眉厚唇或面部饱满，适合驾驭高饱和度的烟熏红唇妆"
        
        # B5: 职场通勤妆（鹅蛋脸或细长眼）
        elif oval_face == 1 or narrow_eyes == 1:
            return "职场通勤妆", "鹅蛋脸或细长眼，大地色眼影加哑光口红，干练不出错"
        
        # B6: 默认 -> 自然裸妆
        else:
            return "自然裸妆", "五官无明显突出特征，伪素颜裸妆最能放大天生优势"


# ==================== 3. 测试入口 ====================
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("💄 妆容推荐引擎测试")
    print("=" * 60)
    
    # 模拟1: 男性，单眼皮，浓眉（顺序与 config.TARGET_ATTRS 一致）
    test_attrs_1 = [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]
    name, reason = recommend_makeup(test_attrs_1)
    print(f"\n👤 用户特征: 男性, 单眼皮, 浓眉")
    print(f"💄 推荐妆容: {name}")
    print(f"📝 推荐理由: {reason}")
    
    # 模拟2: 女性，白皮，鹅蛋脸，弯眉，年轻
    test_attrs_2 = [-1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1]
    name, reason = recommend_makeup(test_attrs_2)
    print(f"\n👤 用户特征: 女性, 白皮, 鹅蛋脸, 弯眉, 年轻")
    print(f"💄 推荐妆容: {name}")
    print(f"📝 推荐理由: {reason}")