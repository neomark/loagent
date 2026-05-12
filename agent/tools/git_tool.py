import subprocess
from .base import Tool
from pydantic import BaseModel, Field

class GitArgs(BaseModel):
    command: str = Field(description="실행할 git 하위 명령어 (예: 'status', 'diff', 'log -5')")

class GitTool(Tool):
    """Git 명령어를 실행하는 도구입니다."""
    name = "git_command"
    description = "Git 명령어를 실행합니다. status, diff, log, add, commit, branch 등을 사용할 수 있습니다."
    args_schema = GitArgs

    # 보안을 위해 허용된 명령어만 실행
    ALLOWED_COMMANDS = {
        "status", "diff", "log", "add", "commit",
        "branch", "show", "stash", "restore", "checkout"
    }

    def run(self, command: str) -> str:
        try:
            # 첫 번째 토큰이 허용된 명령인지 확인
            action = command.strip().split()[0]
            if action not in self.ALLOWED_COMMANDS:
                return (
                    f"보안 상 허용되지 않는 Git 명령: '{action}'\n"
                    f"허용된 명령: {', '.join(sorted(self.ALLOWED_COMMANDS))}"
                )

            result = subprocess.run(
                f"git {command}",
                shell=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=30
            )

            output = result.stdout
            if result.stderr:
                output += result.stderr

            return output if output.strip() else "명령 실행 완료 (출력 없음)"
        except subprocess.TimeoutExpired:
            return "Git 명령 시간 초과 (30초)."
        except Exception as e:
            return f"Git 명령 실행 오류: {str(e)}"
