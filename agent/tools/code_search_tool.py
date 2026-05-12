import subprocess
import os
from .base import Tool
from pydantic import BaseModel, Field

class CodeSearchArgs(BaseModel):
    pattern: str = Field(description="검색할 텍스트 패턴")
    directory: str = Field(default=".", description="검색할 디렉토리 (기본: 현재 디렉토리)")
    file_ext: str = Field(default="*.py", description="검색 대상 파일 확장자 (기본: *.py)")

class CodeSearchTool(Tool):
    """프로젝트 내에서 코드를 검색하는 도구입니다."""
    name = "code_search"
    description = "프로젝트 내에서 텍스트 패턴을 검색합니다. 함수명, 변수명, 문자열 등을 찾을 때 사용하세요."
    args_schema = CodeSearchArgs

    def run(self, pattern: str, directory: str = ".", file_ext: str = "*.py") -> str:
        try:
            # 윈도우 환경: findstr 사용
            cmd = f'findstr /s /n /i "{pattern}" "{directory}\\{file_ext}"'
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                encoding="cp949",
                timeout=30
            )
            output = result.stdout.strip()
            if not output:
                return f"'{pattern}' 패턴에 대한 검색 결과가 없습니다. (검색 범위: {directory}/{file_ext})"

            # 결과가 너무 길면 상위 50줄만 표시
            lines = output.splitlines()
            if len(lines) > 50:
                return "\n".join(lines[:50]) + f"\n... 외 {len(lines) - 50}건 더 있음 (총 {len(lines)}건)"
            return output
        except subprocess.TimeoutExpired:
            return "검색 시간 초과 (30초). 검색 범위를 좁혀주세요."
        except Exception as e:
            return f"코드 검색 오류: {str(e)}"


class ListFilesArgs(BaseModel):
    directory: str = Field(default=".", description="조회할 디렉토리 (기본: 현재 디렉토리)")
    file_ext: str = Field(default="*.py", description="필터할 파일 확장자 (기본: *.py)")

class ListFilesTool(Tool):
    """디렉토리 내 파일 목록을 조회하는 도구입니다."""
    name = "list_files"
    description = "디렉토리 내 파일 목록을 재귀적으로 조회합니다. 프로젝트 구조를 파악할 때 사용하세요."
    args_schema = ListFilesArgs

    def run(self, directory: str = ".", file_ext: str = "*.py") -> str:
        try:
            from pathlib import Path
            path = Path(directory)
            if not path.exists():
                return f"오류: 디렉토리가 존재하지 않습니다: {directory}"

            # 확장자 필터
            ext = file_ext.replace("*", "")
            files = sorted(path.rglob(f"*{ext}"))

            # __pycache__, .git 등 제외
            files = [f for f in files if "__pycache__" not in str(f) and ".git" not in str(f)]

            if not files:
                return f"'{directory}' 경로에 {file_ext} 파일이 없습니다."

            result = [f"디렉토리: {directory} ({len(files)}개 파일)"]
            result.append("-" * 40)
            for f in files:
                rel = f.relative_to(path)
                size = f.stat().st_size
                result.append(f"  {rel} ({size:,} bytes)")

            return "\n".join(result)
        except Exception as e:
            return f"파일 목록 조회 오류: {str(e)}"
