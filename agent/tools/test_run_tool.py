import subprocess
from .base import Tool
from pydantic import BaseModel, Field

class TestRunArgs(BaseModel):
    test_path: str = Field(default="tests/", description="테스트 파일 또는 디렉토리 경로 (기본: tests/)")
    verbose: bool = Field(default=True, description="상세 출력 여부 (기본: True)")
    keyword: str = Field(default="", description="특정 테스트만 실행할 키워드 필터 (예: test_login)")

class TestRunTool(Tool):
    """pytest를 사용하여 테스트를 실행하는 도구입니다."""
    name = "test_run"
    description = "pytest를 사용하여 테스트를 실행합니다. 코드 수정 후 반드시 이 도구로 테스트를 검증하세요."
    args_schema = TestRunArgs

    def run(self, test_path: str = "tests/", verbose: bool = True, keyword: str = "") -> str:
        try:
            cmd = f"python -m pytest {test_path}"
            if verbose:
                cmd += " -v"
            if keyword:
                cmd += f' -k "{keyword}"'

            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=120
            )

            output = result.stdout
            if result.stderr:
                output += f"\n[stderr]:\n{result.stderr}"

            # 결과 요약 추출
            if result.returncode == 0:
                output = "[테스트 성공 ✅]\n" + output
            else:
                output = "[테스트 실패 ❌]\n" + output

            return output
        except subprocess.TimeoutExpired:
            return "테스트 시간 초과 (120초). 무한루프가 있을 수 있습니다."
        except Exception as e:
            return f"테스트 실행 오류: {str(e)}"


class ScriptRunArgs(BaseModel):
    script_path: str = Field(description="실행할 Python 스크립트 경로")
    args: str = Field(default="", description="스크립트에 전달할 인자")

class ScriptRunTool(Tool):
    """Python 스크립트를 직접 실행하는 도구입니다."""
    name = "script_run"
    description = "Python 스크립트 파일을 직접 실행하고 출력을 반환합니다."
    args_schema = ScriptRunArgs

    def run(self, script_path: str, args: str = "") -> str:
        try:
            cmd = f"python {script_path}"
            if args:
                cmd += f" {args}"

            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=60
            )

            output = result.stdout
            if result.stderr:
                output += f"\n[stderr]:\n{result.stderr}"
            if result.returncode != 0:
                output = f"[실행 실패 - 종료코드: {result.returncode}]\n" + output

            return output if output.strip() else "실행 완료 (출력 없음)"
        except subprocess.TimeoutExpired:
            return "스크립트 실행 시간 초과 (60초)."
        except Exception as e:
            return f"스크립트 실행 오류: {str(e)}"
