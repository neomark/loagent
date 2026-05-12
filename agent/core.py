import json
import re
from typing import List, Dict, Any, Optional
from config import get_llm
from .tools.base import ToolRegistry
from .tools.file_tool import FileReadTool, FileWriteTool
from .tools.shell_tool import ShellTool
from .tools.wiki_tool import WikiSearchTool
from .tools.python_tool import PythonTool
from .memory import AgentMemory

REACT_PROMPT = """당신은 유능한 사내 자동화 Agent인 'LOAgent'입니다.
사용자의 요청을 해결하기 위해 도구를 사용하고, 논리적으로 사고하여 행동하십시오.

반드시 한국어로 응답하십시오.

사용 가능한 도구:
{tool_descriptions}

수행 과정 (ReAct 패턴):
1. Thought: 현재 상황을 분석하고 어떤 도구를 사용할지, 또는 최종 답변을 낼지 생각합니다.
2. Action: 사용할 도구의 이름을 적습니다. (예: `wiki_search`)
3. Action Input: 도구에 전달할 인자를 JSON 형식으로 적습니다.
4. Observation: 도구의 실행 결과가 여기에 표시됩니다. (사용자가 제공)
... 위 과정을 반복하여 최종 답변에 도달하면:
5. Final Answer: 사용자의 요청에 대한 최종 답변을 작성합니다.

출력 형식 예시:
Thought: 사용자가 비씨카드 이벤트에 대해 물어봤으므로 위키를 검색해야겠다.
Action: wiki_search
Action Input: {{"query": "비씨카드 이벤트"}}
Observation: (도구 실행 결과)
...
Final Answer: 현재 진행 중인 이벤트는 다음과 같습니다...

시작!

사용자 요청: {input}
{agent_scratchpad}"""

class LOAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.1) # Agent는 일관성을 위해 낮은 온도로 설정
        self.memory = AgentMemory()
        self.registry = ToolRegistry()
        self._setup_tools()

    def _setup_tools(self):
        self.registry.register(FileReadTool())
        self.registry.register(FileWriteTool())
        self.registry.register(ShellTool())
        self.registry.register(WikiSearchTool())
        self.registry.register(PythonTool())

    def _parse_action(self, text: str):
        """LLM 출력에서 Action과 Action Input을 추출합니다."""
        action_match = re.search(r"Action:\s*(.*)", text)
        action_input_match = re.search(r"Action Input:\s*({.*})", text, re.DOTALL)
        
        if action_match and action_input_match:
            return action_match.group(1).strip(), action_input_match.group(1).strip()
        return None, None

    def run(self, user_input: str, max_iterations: int = 5):
        print(f"\n[LOAgent 시작]: {user_input}")
        scratchpad = ""
        
        for i in range(max_iterations):
            # 프롬프트 구성
            prompt = REACT_PROMPT.format(
                tool_descriptions=self.registry.list_tools(),
                input=user_input,
                agent_scratchpad=scratchpad
            )
            
            # LLM 호출
            response = self.llm.invoke(prompt).content
            print(f"\n[Thought/Action {i+1}]:\n{response}")
            
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
                    print(f"\n[Observation]:\n{observation}")
                    scratchpad += f"\n{response}\nObservation: {observation}"
                except Exception as e:
                    observation = f"오류: Action Input을 파싱할 수 없거나 실행 중 오류가 발생했습니다. {str(e)}"
                    print(f"\n[Observation Error]:\n{observation}")
                    scratchpad += f"\n{response}\nObservation: {observation}"
            else:
                # 형식이 맞지 않는 경우 재시도 유도
                error_msg = "오류: 'Action:'과 'Action Input:' 형식을 지켜주세요."
                scratchpad += f"\n{response}\nObservation: {error_msg}"
        
        return "최대 반복 횟수에 도달하여 중단되었습니다."

if __name__ == "__main__":
    agent = LOAgent()
    # CLI 테스트용 루프
    while True:
        query = input("\n사용자 입력 (종료: q): ")
        if query.lower() == 'q':
            break
        result = agent.run(query)
        print(f"\n[최종 답변]:\n{result}")
