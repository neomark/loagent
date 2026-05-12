import json
import os
from datetime import datetime
from typing import List, Dict, Any

class AgentMemory:
    """Agent의 대화 및 작업 이력을 관리합니다."""
    
    def __init__(self, file_path: str = "data/agent_memory.jsonl"):
        self.file_path = file_path
        self.history: List[Dict[str, Any]] = []
        self._load_memory()

    def _load_memory(self):
        """기존 이력을 로드합니다."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        self.history.append(json.loads(line))
            except Exception as e:
                print(f"메모리 로드 중 오류: {e}")

    def add_message(self, role: str, content: str, **kwargs):
        """메시지를 메모리에 추가하고 파일에 저장합니다."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content,
            **kwargs
        }
        self.history.append(entry)
        
        # 파일에 추가 (Append mode)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def get_recent_context(self, limit: int = 10) -> List[Dict[str, str]]:
        """최근 대화 맥락을 반환합니다."""
        return [{"role": h["role"], "content": h["content"]} for h in self.history[-limit:]]

    def clear(self):
        """메모리를 초기화합니다."""
        self.history = []
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
