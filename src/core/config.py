import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API 密钥
    API_KEY: str = os.getenv("API_KEY", "sk-86e40a12cbeb460fa469be2cba206631")
    API_URL: str = os.getenv("API_URL", "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation")
    
    # 模型路径
    MODEL_PATH: str = os.getenv("MODEL_SAVE_PATH", "./models/best_model_end2end.pth")
    
    # 服务配置
    DEVICE: str = os.getenv("DEVICE", "cpu")
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", 8000))

settings = Settings()


#14 个面部属性
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
# 属性数量
NUM_ATTRS = len(TARGET_ATTRS)
#模型超参数
INPUT_DIM = 513      # 512 特征 + 1 性别
HIDDEN_DIMS = [256, 128]
OUTPUT_DIM = NUM_ATTRS