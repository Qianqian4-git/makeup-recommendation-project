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
from src.inference import predict

app = FastAPI(
    title="💄 妆容推荐 API",
    description="上传自拍照，AI 分析面部特征并推荐最适合的妆容",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


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
        raise HTTPException(
            status_code = 400,
            detail = "❌ 不支持的文件类型,(jpg, jpeg, png, bmp, gif)"
        )
    # 2. 保存临时文件
    try:
        with tempfile.NamedTemporaryFile(delete = false,suffix='.jpg') as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail = f"❌ 文件保存失败: {str(e)}"
        )
    # 3. 调用推理函数（默认自动检测性别）
    try:
        result = predict(tmp_path,gender = None)
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
    return JSONResponse(content = {
        "makeup": result["makeup"],
        "reason": result["reason"],
        "attributes": result["attributes"],
        "filename": file.filename
    })

if __name__ == "__main__":
    uvicorn.run(
        "fastapi_app:app",
        host = '0.0.0.0',
        port = 8000,
        reload = True  # 开发模式，代码变动自动重启
    )