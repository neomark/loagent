from pathlib import Path
from .base import Tool
from pydantic import BaseModel, Field

class CodeEditArgs(BaseModel):
    file_path: str = Field(description="편집할 소스 파일 경로")
    start_line: int = Field(description="치환 시작 라인 번호")
    end_line: int = Field(description="치환 끝 라인 번호 (이 라인 포함)")
    new_content: str = Field(description="새로 넣을 코드 내용")

class CodeInsertArgs(BaseModel):
    file_path: str = Field(description="삽입할 소스 파일 경로")
    after_line: int = Field(description="이 라인 뒤에 삽입 (0이면 파일 맨 앞)")
    new_content: str = Field(description="삽입할 코드 내용")

class CodeEditTool(Tool):
    """소스 코드의 특정 라인 범위를 새 코드로 교체하는 도구입니다."""
    name = "code_edit"
    description = "소스 코드의 특정 라인 범위(start_line~end_line)를 새 코드로 교체합니다. 수정 전에 반드시 code_read로 현재 코드를 확인하세요."
    args_schema = CodeEditArgs

    def run(self, file_path: str, start_line: int, end_line: int, new_content: str) -> str:
        try:
            path = Path(file_path)
            if not path.exists():
                return f"오류: 파일이 존재하지 않습니다: {file_path}"

            lines = path.read_text(encoding="utf-8").splitlines()
            total = len(lines)

            if start_line < 1 or start_line > total:
                return f"오류: 시작 라인({start_line})이 유효 범위(1~{total})를 벗어납니다."
            if end_line < start_line or end_line > total:
                return f"오류: 끝 라인({end_line})이 유효 범위({start_line}~{total})를 벗어납니다."

            new_lines = new_content.splitlines()
            old_count = end_line - start_line + 1
            lines[start_line - 1:end_line] = new_lines

            path.write_text("\n".join(lines) + "\n", encoding="utf-8")

            return (
                f"편집 완료: {file_path}\n"
                f"  변경 범위: 라인 {start_line}~{end_line} ({old_count}줄 → {len(new_lines)}줄)\n"
                f"  현재 전체: {len(lines)}줄"
            )
        except Exception as e:
            return f"코드 편집 오류: {str(e)}"

class CodeInsertTool(Tool):
    """소스 코드의 특정 위치에 새 코드를 삽입하는 도구입니다."""
    name = "code_insert"
    description = "소스 코드의 지정된 라인 뒤에 새 코드를 삽입합니다. after_line=0이면 파일 맨 앞에 삽입합니다."
    args_schema = CodeInsertArgs

    def run(self, file_path: str, after_line: int, new_content: str) -> str:
        try:
            path = Path(file_path)
            if not path.exists():
                # 새 파일 생성
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(new_content + "\n", encoding="utf-8")
                return f"새 파일 생성 완료: {file_path} ({len(new_content.splitlines())}줄)"

            lines = path.read_text(encoding="utf-8").splitlines()
            new_lines = new_content.splitlines()

            if after_line < 0 or after_line > len(lines):
                return f"오류: 삽입 위치({after_line})가 유효 범위(0~{len(lines)})를 벗어납니다."

            lines[after_line:after_line] = new_lines
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")

            return (
                f"삽입 완료: {file_path}\n"
                f"  삽입 위치: 라인 {after_line} 뒤 ({len(new_lines)}줄 추가)\n"
                f"  현재 전체: {len(lines)}줄"
            )
        except Exception as e:
            return f"코드 삽입 오류: {str(e)}"
