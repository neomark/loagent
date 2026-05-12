import json
import re
from config import get_llm
from .tools.base import ToolRegistry
from .tools.code_read_tool import CodeReadTool
from .tools.code_edit_tool import CodeEditTool, CodeInsertTool
from .tools.code_search_tool import CodeSearchTool, ListFilesTool
from .tools.test_run_tool import TestRunTool, ScriptRunTool
from .tools.git_tool import GitTool
from .tools.file_tool import FileReadTool, FileWriteTool
from .memory import AgentMemory

CODING_PROMPT = """당신은 숙련된 소프트웨어 개발자 에이전트 'LOCoder'입니다.
사용자의 코딩 요청을 받아 소스 코드를 분석, 수정, 테스트합니다.
반드시 한국어로 응답하십시오.

## 작업 원칙
1. 코드를 수정하기 전에 반드시 code_read로 현재 코드를 먼저 확인합니다.
2. 수정 후에는 가능하면 test_run으로 테스트를 실행하여 검증합니다.
3. 테스트가 실패하면, 에러 메시지를 분석하고 코드를 다시 수정합니다.
4. 모든 작업이 완료되면 변경 사항을 요약합니다.

## 작업 흐름 (권장 순서)
1. list_files로 프로젝트 구조 파악
2. code_search로 관련 코드 위치 검색
3. code_read로 대상 코드 확인
4. code_edit 또는 code_insert로 코드 수정/추가
5. test_run 또는 script_run으로 검증
6. git_command로 변경 사항 확인 (선택)
7. Final Answer로 변경 내용 요약 보고

## 사용 가능한 도구
{tool_descriptions}

## 수행 과정 (ReAct 패턴)
Thought: 현재 상황을 분석하고 다음 행동을 계획합니다.
Action: 사용할 도구 이름
Action Input: {{"key": "value"}} (JSON 형식)
Observation: (도구 실행 결과)
... (반복)
Final Answer: 최종 결과 보고

시작!

사용자 요청: {input}
{agent_scratchpad}"""


class CodingAgent:
    """코딩 전용 에이전트입니다. 소스 코드 편집, 테스트, Git 관리를 수행합니다."""

    def __init__(self):
        self.llm = get_llm(temperature=0.1, max_tokens=4096)
        self.memory = AgentMemory(file_path="data/coding_memory.jsonl")
        self.registry = ToolRegistry()
        self._setup_tools()

    def _setup_tools(self):
        """코딩 전용 도구를 등록합니다."""
        # 코드 분석 도구
        self.registry.register(CodeReadTool())
        self.registry.register(CodeSearchTool())
        self.registry.register(ListFilesTool())
        # 코드 편집 도구
        self.registry.register(CodeEditTool())
        self.registry.register(CodeInsertTool())
        # 실행/테스트 도구
        self.registry.register(TestRunTool())
        self.registry.register(ScriptRunTool())
        # 파일/Git 도구
        self.registry.register(FileReadTool())
        self.registry.register(FileWriteTool())
        self.registry.register(GitTool())

    def _parse_action(self, text: str):
        """LLM 출력에서 Action과 Action Input을 추출합니다."""
        action_match = re.search(r"Action:\s*(.*)", text)
        action_input_match = re.search(r"Action Input:\s*({.*})", text, re.DOTALL)

        if action_match and action_input_match:
            return action_match.group(1).strip(), action_input_match.group(1).strip()
        return None, None

    def run(self, user_input: str, max_iterations: int = 10) -> str:
        """에이전트 실행. 코딩 작업은 여러 단계가 필요하므로 기본 반복 횟수를 10으로 설정."""
        print(f"\n[LOCoder 시작]: {user_input}")
        scratchpad = ""

        for i in range(max_iterations):
            prompt = CODING_PROMPT.format(
                tool_descriptions=self.registry.list_tools(),
                input=user_input,
                agent_scratchpad=scratchpad
            )

            response = self.llm.invoke(prompt).content
            print(f"\n[Step {i + 1}]:\n{response}")

            # 최종 답변 확인
            if "Final Answer:" in response:
                final_answer = response.split("Final Answer:")[-1].strip()
                self.memory.add_message("user", user_input)
                self.memory.add_message("assistant", final_answer)
                return final_answer

            # Action 추출 및 실행
            action_name, action_input_str = self._parse_action(response)
            if action_name and action_input_str:
                try:
                    action_input = json.loads(action_input_str)
                    observation = self.registry.run_tool(action_name, action_input)
                    print(f"\n[Observation]:\n{observation[:500]}")
                    scratchpad += f"\n{response}\nObservation: {observation}"
                except json.JSONDecodeError as e:
                    error_msg = f"JSON 파싱 오류: {str(e)}. Action Input은 올바른 JSON이어야 합니다."
                    scratchpad += f"\n{response}\nObservation: {error_msg}"
                except Exception as e:
                    error_msg = f"도구 실행 중 오류: {str(e)}"
                    scratchpad += f"\n{response}\nObservation: {error_msg}"
            else:
                scratchpad += f"\n{response}\nObservation: 'Action:'과 'Action Input:' 형식을 지켜주세요."

        return "최대 반복 횟수에 도달하여 중단되었습니다. 지금까지의 작업을 확인해주세요."


if __name__ == "__main__":
    agent = CodingAgent()
    while True:
        query = input("\n[LOCoder] 코딩 요청 (종료: q): ")
        if query.lower() == "q":
            break
        result = agent.run(query)
        print(f"\n[최종 결과]:\n{result}")
