<<<<<<< HEAD
# ============================================================
# DEPRECATED (弃用)
# 功能: 旧版 FastAPI 应用入口（集成所有路由的单一文件）
# 替代方案: 请使用模块化架构:
#   - 入口: src/api/main.py
#   - 路由: src/api/routers/predict.py, src/api/routers/chat.py
#   - 服务: src/services/ 下的业务逻辑
# 弃用原因: 代码过于耦合，难以维护和扩展。
# 归档日期: 2026-08-06
# ============================================================


import os
import sys
import tempfile
import requests
import json
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from src.inference_end2end import predict_image

app = FastAPI(title="Klea · AI 美妆助手", version="1.0.0")
=======
import os
import sys
from pathlib import Path

# ===== 先把项目根目录加到 Python 路径（在所有 src 导入之前） =====
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

import tempfile
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# 现在可以导入 src 下的模块了
from src.inference_end2end import predict_image

app = FastAPI(
    title="💄 妆容推荐 API",
    description="上传自拍照，AI 分析面部特征并推荐最适合的妆容",
    version="3.0.0"
)
>>>>>>> a3ac313 (chore: 归档旧版 fastapi_app.py 至 legacy- fastapi_app.py 已被模块化架构替代- 添加 DEPRECATED 注释说明替代方案)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD
# ===== 全局变量：存储最近一次推荐 =====
latest_recommendation = None

# ===== 妆容推荐 =====
=======
>>>>>>> a3ac313 (chore: 归档旧版 fastapi_app.py 至 legacy- fastapi_app.py 已被模块化架构替代- 添加 DEPRECATED 注释说明替代方案)
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "bmp", "gif"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

<<<<<<< HEAD
@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

@app.post("/predict")
async def predict_api(file: UploadFile = File(...)):
    global latest_recommendation
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="不支持的文件类型")
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
=======

@app.get("/")
async def root():
    return{
         "message": "💄 妆容推荐 API 服务已启动",
        "docs": "/docs",
        "endpoints": {
            "/predict": "POST 上传图片，返回妆容推荐"
        }
    }

@app.post("/predict")
async def predict_api(file:UploadFile = File(...)):
     # 1. 校验文件格式
    if not allowed_file(file.filename):
        print(f"❌ 文件格式被拒: {file.filename}, content_type: {file.content_type}")
        raise HTTPException(
            status_code = 400,
            detail = "❌ 不支持的文件类型,(jpg, jpeg, png, bmp, gif)"
        )
    # 2. 保存临时文件
    try:
        with tempfile.NamedTemporaryFile(delete = False,suffix='.jpg') as tmp:
>>>>>>> a3ac313 (chore: 归档旧版 fastapi_app.py 至 legacy- fastapi_app.py 已被模块化架构替代- 添加 DEPRECATED 注释说明替代方案)
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
    except Exception as e:
<<<<<<< HEAD
        raise HTTPException(status_code=500, detail=f"文件保存失败: {str(e)}")
    try:
        makeup, reason = predict_image(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推理失败: {str(e)}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    # --- 构造结构化推荐数据（模拟，后续可替换为真实输出） ---
    # 从 reason 中提取特征描述（简单方法）
    import re
    feature_match = re.search(r"您拥有(.*?)。", reason)
    features = feature_match.group(1) if feature_match else "匀称的五官"
    # 根据妆容名称映射一些虚拟数据（演示用）
    makeup_map = {
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
    default_data = {"face_shape": "匀称", "skin_tone": "中性", "shade": "NARS #Orgasm", "match": 75}
    data = makeup_map.get(makeup, default_data)
    
    # 合并特征描述
    data["features"] = features
    data["makeup_name"] = makeup
    data["reason"] = reason

    # 存储到全局变量
    latest_recommendation = data

    return JSONResponse(content={
        "makeup": makeup,
        "reason": reason,
        "face_shape": data["face_shape"],
        "skin_tone": data["skin_tone"],
        "shade": data["shade"],
        "match": data["match"],
        "features": features,
        "filename": file.filename
    })

# ===== AI 聊天 =====
API_KEY = "sk-86e40a12cbeb460fa469be2cba206631"
API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
conversation_history = []

@app.post("/api/chat")
async def chat_api(question: str = Form(...)):
    global conversation_history, latest_recommendation
    # 如果存在最近的推荐结果，将其作为上下文注入（但不直接追加到历史，而是作为系统提示）
    context_message = None
    if latest_recommendation:
        makeup_name = latest_recommendation.get("makeup_name", "")
        face_shape = latest_recommendation.get("face_shape", "")
        skin_tone = latest_recommendation.get("skin_tone", "")
        shade = latest_recommendation.get("shade", "")
        context_message = f"用户最近一次妆容推荐为【{makeup_name}】，脸型{face_shape}，肤色{skin_tone}，推荐色号{shade}。请基于此信息回答用户的问题。"
    
    # 构建消息列表
    messages = []
    if context_message:
        messages.append({"role": "system", "content": context_message})
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": question})
    
    # 限制上下文长度
    MAX_CONTEXT_CHARS = 2000
    # 简单截断（保留最近的消息）
    while len(messages) > 1 and sum(len(m["content"]) for m in messages) > MAX_CONTEXT_CHARS:
        # 移除最早的用户消息（跳过系统消息）
        if len(messages) > 2:
            messages.pop(1)
        else:
            break

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "qwen-turbo",
        "input": {"messages": messages},
        "parameters": {"result_format": "message"}
    }
    try:
        resp = requests.post(API_URL, json=payload, headers=headers)
        resp.raise_for_status()
        res_data = resp.json()
        answer = res_data["output"]["choices"][0]["message"]["content"]
        # 只保存用户和assistant的对话历史（不含系统消息）
        conversation_history.append({"role": "user", "content": question})
        conversation_history.append({"role": "assistant", "content": answer})
        # 限制历史长度
        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]
        return {"code": 200, "answer": answer}
    except Exception as e:
        return {"code": 500, "error": str(e)}

if __name__ == "__main__":
    uvicorn.run("fastapi_app:app", host="127.0.0.1", port=8000, reload=True)
=======
        raise HTTPException(
            status_code = 500,
            detail = f"❌ 文件保存失败: {str(e)}"
        )
    # 3. 调用推理函数（默认自动检测性别）
    try:
        makeup, reason = predict_image(tmp_path)
        print(f"🔍 API 推理结果: makeup={makeup}, reason={reason[:50]}...")
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail = f"❌ 推理失败: {str(e)}"
        )
         # 清理临时文件
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    
    # 4. 返回结果
    return JSONResponse(content={
    "makeup": makeup,
    "reason": reason,
    "filename": file.filename
})

if __name__ == "__main__":
    uvicorn.run(
        "fastapi_app:app",
        host = '0.0.0.0',
        port = 8000,
        reload = True  # 开发模式，代码变动自动重启
    )
>>>>>>> a3ac313 (chore: 归档旧版 fastapi_app.py 至 legacy- fastapi_app.py 已被模块化架构替代- 添加 DEPRECATED 注释说明替代方案)
