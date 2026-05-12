from pathlib import Path
from .base import Tool
from pydantic import BaseModel, Field

class CodeReadArgs(BaseModel):
    file_path: str = Field(description="읽을 소스 파일 경로")
    start_line: int = Field(default=1, description="시작 라인 번호 (기본: 1)")
    end_line: int = Field(default=-1, description="끝 라인 번호 (기본: -1이면 끝까지)")

class CodeReadTool(Tool):
    """소스 코드를 라인 번호와 함께 읽는 도구입니다."""
    name = "code_read"
    description = "소스 코드 파일을 라인 번호와 함께 읽습니다. 코드를 수정하기 전에 반드시 먼저 사용하세요."
    args_schema = CodeReadArgs

    def run(self, file_path: str, start_line: int = 1, end_line: int = -1) -> str:
        try:
            path = Path(file_path)
            if not path.exists():
                return f"오류: 파일이 존재하지 않습니다: {file_path}"

            lines = path.read_text(encoding="utf-8").splitlines()
            total = len(lines)

            if end_line == -1:
                end_line = total

            # 범위 보정
            start_line = max(1, start_line)
            end_line = min(end_line, total)

            if start_line > total:
                return f"오류: 시작 라인({start_line})이 전체 라인 수({total})를 초과합니다."

            result = [f"파일: {file_path} (전체 {total}줄, 표시: {start_line}-{end_line}줄)"]
            result.append("-" * 60)
            for i in range(start_line - 1, end_line):
                result.append(f"{i + 1:4d} | {lines[i]}")
            result.append("-" * 60)

            return "\n".join(result)
        except Exception as e:
            return f"코드 읽기 오류: {str(e)}"
