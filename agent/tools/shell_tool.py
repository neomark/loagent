import subprocess
from .base import Tool
from pydantic import BaseModel, Field

class ShellArgs(BaseModel):
    command: str = Field(description="실행할 터미널 명령어")

class ShellTool(Tool):
    name = "shell_execute"
    description = "터미널 명령어를 실행하고 결과를 반환합니다. 윈도우 환경을 고려하여 실행됩니다."
    args_schema = ShellArgs

    def run(self, command: str) -> str:
        try:
            # 윈도우 환경을 고려하여 shell=True 설정
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                encoding="cp949" # 윈도우 기본 인코딩 고려
            )
            output = result.stdout
            if result.stderr:
                output += f"\n[에러 출력]:\n{result.stderr}"
            return output if output else "명령어 실행 완료 (출력 없음)"
        except Exception as e:
            return f"명령어 실행 중 오류 발생: {str(e)}"
