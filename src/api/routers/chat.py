from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse

from src.services.chat_service import chat_service

router = APIRouter()

@router.post("/api/chat")
async def chat(question: str = Form(...)):
    try:
        answer = chat_service.chat(question)
        return JSONResponse(content={"code": 200, "answer": answer})
    except Exception as e:
        return JSONResponse(content={"code": 500, "error": str(e)})