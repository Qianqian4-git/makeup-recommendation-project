from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from src.services.recommendation import process_image

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="不支持的文件类型")
    try:
        content = await file.read()
        result = process_image(content, file.filename)
        return JSONResponse(content={
            "makeup": result["makeup"],
            "reason": result["reason"],
            "face_shape": result["face_shape"],
            "skin_tone": result["skin_tone"],
            "shade": result["shade"],
            "match": result["match"],
            "features": result["features"],
            "filename": file.filename
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))