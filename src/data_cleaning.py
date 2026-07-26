import os
import logging
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(level=logging.INFO)

# 加载 .env 文件
load_dotenv()

# 从 .env 文件中读取路径
raw_data_dir = os.getenv("RAW_DATA_DIR")
processed_data_dir = os.getenv("PROCESSED_DATA_DIR")
model_save_path = os.getenv("MODEL_SAVE_PATH")
features_save_path = os.getenv("FEATURES_SAVE_PATH")

# 检查路径是否正确加载
if not raw_data_dir or not processed_data_dir:
    raise ValueError("请检查 .env 文件，确保 RAW_DATA_DIR 和 PROCESSED_DATA_DIR 已正确配置！")

# 确保目录存在
os.makedirs(processed_data_dir, exist_ok=True)
os.makedirs(os.path.dirname(model_save_path), exist_ok=True)  # 确保模型保存目录存在
os.makedirs(os.path.dirname(features_save_path), exist_ok=True)  # 确保特征保存目录存在

# 打印路径以验证
logging.info(f"原始数据路径: {raw_data_dir}")
logging.info(f"处理后数据路径: {processed_data_dir}")
logging.info(f"模型保存路径: {model_save_path}")
logging.info(f"特征保存路径: {features_save_path}")