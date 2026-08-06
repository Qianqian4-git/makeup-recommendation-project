import tempfile
import os
import re
from typing import Dict, Any

from src.inference_end2end import predict_image
from src.services.context_store import context_store

MAKEUP_META = {
    "韩系水光妆": {"face_shape": "鹅蛋脸", "skin_tone": "冷白皮", "shade": "兰蔻 #01", "match": 92},
    "日系元气妆": {"face_shape": "圆脸", "skin_tone": "暖黄皮", "shade": "3CE #Pink", "match": 88},
    "亚裔混血妆": {"face_shape": "高颧骨", "skin_tone": "中性皮", "shade": "MAC #Chili", "match": 85},
    "职场通勤妆": {"face_shape": "鹅蛋脸", "skin_tone": "中性偏暖", "shade": "NARS #DolceVita", "match": 90},
    "千金妆": {"face_shape": "立体轮廓", "skin_tone": "冷白皮", "shade": "YSL #21", "match": 93},
    "新中式妆": {"face_shape": "东方古典", "skin_tone": "暖白皮", "shade": "毛戈平 #602", "match": 87},
    "轻泰妆": {"face_shape": "混血感", "skin_tone": "中性偏冷", "shade": "3CE #Taupe", "match": 89},
    "美式慵懒雀斑妆": {"face_shape": "随性", "skin_tone": "暖黄皮", "shade": "Glossier #Cloud", "match": 84},
    "自然裸妆": {"face_shape": "自然", "skin_tone": "中性", "shade": "Bobbi Brown #Brown", "match": 80},
    "韩系欧巴妆": {"face_shape": "清秀", "skin_tone": "冷白皮", "shade": "LANCOME #Bo-02", "match": 90},
    "硬朗轮廓妆": {"face_shape": "硬朗", "skin_tone": "暖皮", "shade": "MAC #Velvet", "match": 86},
    "自然净澈妆": {"face_shape": "清爽", "skin_tone": "中性", "shade": "NARS #Sheer", "match": 82},
    "日系盐系妆": {"face_shape": "少年感", "skin_tone": "冷白皮", "shade": "SUQQU #01", "match": 88},
}

def process_image(file_content: bytes, filename: str) -> Dict[str, Any]:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(file_content)
        tmp_path = tmp.name

    try:
        makeup, reason = predict_image(tmp_path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    feature_match = re.search(r"您拥有(.*?)。", reason)
    features = feature_match.group(1) if feature_match else "匀称的五官"
    meta = MAKEUP_META.get(makeup, {"face_shape": "匀称", "skin_tone": "中性", "shade": "NARS #Orgasm", "match": 75})

    result = {
        "makeup": makeup,
        "reason": reason,
        "features": features,
        "face_shape": meta["face_shape"],
        "skin_tone": meta["skin_tone"],
        "shade": meta["shade"],
        "match": meta["match"],
    }
    context_store.set_recommendation(result)
    return result