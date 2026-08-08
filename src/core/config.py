import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API 密钥
    API_KEY: str = os.getenv("API_KEY")
    API_URL: str = os.getenv("API_URL", "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation")
    
    # 模型路径
    MODEL_PATH: str = os.getenv("MODEL_SAVE_PATH", "./models/best_model_end2end.pth")
    
    # 服务配置
    DEVICE: str = os.getenv("DEVICE", "cpu")
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", 8000))

settings = Settings()

# 启动时检查 API_KEY 是否设置
if not settings.API_KEY:
    raise ValueError("❌ API_KEY 未在 .env 中设置！请检查 .env 文件。")