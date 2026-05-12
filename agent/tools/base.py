from abc import ABC, abstractmethod
from typing import Dict, Any, Type
from pydantic import BaseModel

class Tool(ABC):
    """모든 도구의 기본 클래스입니다."""
    
    name: str
    description: str
    args_schema: Type[BaseModel] = None

    @abstractmethod
    def run(self, **kwargs) -> str:
        """도구를 실행하고 결과를 문자열로 반환합니다."""
        pass

class ToolRegistry:
    """도구들을 관리하고 실행하는 레지스트리입니다."""
    
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self._tools[tool.name] = tool
        print(f"도구 등록됨: {tool.name}")

    def get_tool(self, name: str) -> Tool:
        return self._tools.get(name)

    def list_tools(self) -> str:
        return "\n".join([f"- {name}: {tool.description}" for name, tool in self._tools.items()])

    def run_tool(self, name: str, args: Dict[str, Any]) -> str:
        tool = self.get_tool(name)
        if not tool:
            return f"오류: '{name}' 도구를 찾을 수 없습니다."
        try:
            return tool.run(**args)
        except Exception as e:
            return f"도구 '{name}' 실행 중 오류 발생: {str(e)}"
