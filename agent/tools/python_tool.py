import sys
import io
from .base import Tool
from pydantic import BaseModel, Field

class PythonArgs(BaseModel):
    code: str = Field(description="실행할 Python 코드")

class PythonTool(Tool):
    name = "python_execute"
    description = "Python 코드를 실행하고 표준 출력을 반환합니다. 데이터 분석이나 계산에 유용합니다."
    args_schema = PythonArgs

    def run(self, code: str) -> str:
        # 표준 출력을 가로채기 위한 설정
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        
        try:
            # 코드 실행
            exec(code, globals())
            sys.stdout = old_stdout
            return redirected_output.getvalue()
        except Exception as e:
            sys.stdout = old_stdout
            return f"Python 코드 실행 중 오류 발생: {str(e)}"
