import requests
from typing import List, Dict

from src.core.config import settings
from src.services.context_store import context_store

class ChatService:
    def __init__(self):
        self.conversation_history: List[Dict[str, str]] = []

    def chat(self, question: str) -> str:
        messages = []
        rec = context_store.get_recommendation()
        if rec:
            context_msg = (
                f"用户最近一次妆容推荐为【{rec.get('makeup', '')}】，"
                f"脸型{rec.get('face_shape', '')}，肤色{rec.get('skin_tone', '')}，"
                f"推荐色号{rec.get('shade', '')}。请基于此信息回答。"
            )
            messages.append({"role": "system", "content": context_msg})

        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": question})

        payload = {
            "model": "qwen-turbo",
            "input": {"messages": messages},
            "parameters": {"result_format": "message"}
        }
        headers = {"Authorization": f"Bearer {settings.API_KEY}", "Content-Type": "application/json"}

        try:
            resp = requests.post(settings.API_URL, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            answer = data["output"]["choices"][0]["message"]["content"]
            self.conversation_history.append({"role": "user", "content": question})
            self.conversation_history.append({"role": "assistant", "content": answer})
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            return answer
        except Exception as e:
            return f"AI 服务异常: {str(e)}"

chat_service = ChatService()