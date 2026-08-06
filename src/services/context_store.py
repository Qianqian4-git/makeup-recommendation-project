from typing import Optional, Dict, Any

class ContextStore:
    _instance = None
    _latest_recommendation: Optional[Dict[str, Any]] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def set_recommendation(self, data: Dict[str, Any]):
        self._latest_recommendation = data

    def get_recommendation(self) -> Optional[Dict[str, Any]]:
        return self._latest_recommendation

context_store = ContextStore()