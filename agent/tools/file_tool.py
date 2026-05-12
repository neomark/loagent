import os
from pathlib import Path
from .base import Tool
from pydantic import BaseModel, Field

class FileReadArgs(BaseModel):
    file_path: str = Field(description="읽을 파일의 경로")

class FileWriteArgs(BaseModel):
    file_path: str = Field(description="저장할 파일의 경로")
    content: str = Field(description="저장할 내용")

class FileReadTool(Tool):
    name = "file_read"
    description = "파일의 내용을 읽습니다."
    args_schema = FileReadArgs

    def run(self, file_path: str) -> str:
        try:
            path = Path(file_path)
            if not path.exists():
                return f"오류: 파일이 존재하지 않습니다: {file_path}"
            return path.read_text(encoding="utf-8")
        except Exception as e:
            return f"파일 읽기 오류: {str(e)}"

class FileWriteTool(Tool):
    name = "file_write"
    description = "파일에 내용을 씁니다. 파일이 없으면 새로 생성합니다."
    args_schema = FileWriteArgs

    def run(self, file_path: str, content: str) -> str:
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return f"파일 저장 완료: {file_path}"
        except Exception as e:
            return f"파일 쓰기 오류: {str(e)}"
