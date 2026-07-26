import os
import logging
import pandas as pd
from PIL import Image
from tqdm import tqdm
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 加载.env文件
load_dotenv()

# 从.env文件读取路径
RAW_DATA_DIR = os.getenv("RAW_DATA_DIR")
PROCESSED_DATA_DIR = os.getenv("PROCESSED_DATA_DIR")
MODEL_SAVE_PATH = os.getenv("MODEL_SAVE_PATH")
FEATURES_SAVE_PATH = os.getenv("FEATURES_SAVE_PATH")

# 检查必要路径
if not RAW_DATA_DIR or not PROCESSED_DATA_DIR or not MODEL_SAVE_PATH or not FEATURES_SAVE_PATH:
    logging.error("必要的环境变量未设置，请检查.env文件。")
    raise ValueError("必要的环境变量未设置，请检查.env文件。")


# 确保目录存在
os.makedirs(PROCESSED_DATA_DIR,exist_ok=True)
os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
os.makedirs(os.path.dirname(FEATURES_SAVE_PATH), exist_ok=True)

# 打印路径以验证
logging.info(f"原始数据路径：{RAW_DATA_DIR}")
logging.info(f"处理后数据路径：{PROCESSED_DATA_DIR}")
logging.info(f"模型保存路径：{MODEL_SAVE_PATH}")
logging.info(f"特征保存路径：{FEATURES_SAVE_PATH}")


# 数据清洗函数
def clean_celeba_data(limit: int = None):
    """
    清洗 CelebA 数据集：
    1. 自动定位 list_attr_celeba.txt（在图片文件夹的父目录）
    2. 检查每张图片是否存在且可读取
    3. 保存有效图片列表到 processed_data_dir
    """
    logging.info("=" * 50)
    logging.info("🧹 开始数据清洗...")
    logging.info("=" * 50)

    # 1. 自动定位属性文件（在 RAW_DATA_DIR 的父目录下）
    parent_dir = os.path.dirname(RAW_DATA_DIR)
    attr_file = os.path.join(parent_dir,"list_attr_celeba.txt")

    if not os.path.exists(attr_file):
        raise FileNotFoundError(f"❌ 找不到属性文件：{attr_file}，请确认它位于 {parent_dir} 下。")
    
    logging.info(f"✅ 找到属性文件：{attr_file}")

    # 2. 检查图片目录
    if not os.path.exists(RAW_DATA_DIR):
        raise FileNotFoundError(f"❌ 找不到图片目录：{RAW_DATA_DIR}，请确认它存在。")

    # 3. 读取属性文件

    try:
       attr_df = pd.read_csv(attr_file, sep = r'\s+',skiprows = 2,dtype = str)
       attr_df = attr_df.rename(columns={attr_df.columns[0]:"filename"})
    except Exception as e:
        logging.error(f"❌ 读取属性文件失败：{e}")
        raise
  
        # 取子集（测试用）
    if limit:
        attr_df = attr_df.head(limit)

    total_count = len(attr_df)
    logging.info(f"待检查的图片总数：{total_count}")

    # 4. 检查每张图片是否存在且可读取
    
    valid_images = []
    corrupt_images = []

    for idx , row in tqdm(attr_df.iterrows(),total = total_count, desc = "检查图片"):
       img_name = row['filename']
       img_path = os.path.join(RAW_DATA_DIR,img_name)    

       try :
          with Image.open(img_path) as img :
               # 强制转换为RGB模式，以检测损坏
                img.convert('RGB')
                valid_images.append(img_name)
       except Exception as e:
        corrupt_images.append({img_name,str(e)})

    # 5. 统计结果
    valid_count = len(valid_images)
    corrupt_count = len(corrupt_images)
    logging.info(f"✅ 有效图片数量：{valid_count}")
    logging.info(f"❌ 损坏图片数量：{corrupt_count}")
    if total_count > 0:
        logging.info(f"📊 成功率：{valid_count / total_count * 100:.2f}%")
        logging.info(f"损坏率：{corrupt_count/total_count * 100:.2f}%")
    
    # 6. 保存清洗结果
    valid_df= pd.DataFrame(valid_images,columns=["filename"])
    valid_csv_path = os.path.join(PROCESSED_DATA_DIR,"valid_images.csv")
    valid_df.to_csv(valid_csv_path,index=False)
    logging.info(f"✅ 有效图片列表已保存到：{valid_csv_path}")

    if corrupt_count > 0:
        corrupt_df = pd.DataFrame(corrupt_images,columns=["filename","error"])
        corrupt_csv_path = os.path.join(PROCESSED_DATA_DIR,"corrupt_images.csv")
        corrupt_df.to_csv(corrupt_csv_path,index=False)
        logging.info(f"❌ 损坏图片列表已保存到：{corrupt_csv_path}")
    

    logging.info("=" * 50)
    logging.info("🧹 数据清洗完成！")
    return valid_df , corrupt_images



if __name__ == "__main__":
    # 测试数据清洗函数
    clean_celeba_data(limit=None) 