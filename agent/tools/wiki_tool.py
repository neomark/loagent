import os
import subprocess
from .base import Tool
from pydantic import BaseModel, Field

class WikiSearchArgs(BaseModel):
    query: str = Field(description="위키에서 검색할 질의어")

class WikiSearchTool(Tool):
    name = "wiki_search"
    description = "사내 LLM Wiki(OpenKB)에서 정보를 검색합니다."
    args_schema = WikiSearchArgs

    def run(self, query: str) -> str:
        try:
            kb_dir = os.path.join(os.getcwd(), "kb")
            if not os.path.exists(kb_dir):
                return "오류: 'kb' 디렉토리가 존재하지 않습니다. 먼저 위키를 초기화해주세요."
            
            # openkb query 명령 실행 (UTF-8 인코딩 설정 포함)
            result = subprocess.run(
                f"openkb query \"{query}\"",
                shell=True,
                cwd=kb_dir,
                capture_output=True,
                text=True,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"}
            )
            
            if result.returncode != 0:
                return f"위키 검색 중 오류 발생: {result.stderr}"
            
            return result.stdout
        except Exception as e:
            return f"위키 검색 도구 실행 중 예외 발생: {str(e)}"
