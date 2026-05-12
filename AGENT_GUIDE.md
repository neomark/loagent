# LOAgent 사용 및 확장 가이드

LOAgent는 사용자의 지시를 받아 스스로 생각(Thought)하고 적절한 도구(Tool)를 사용하여 작업을 수행하는 ReAct 패턴 기반의 자율 에이전트입니다.

---

## 1. Agent 실행 및 사용법

LOAgent는 두 가지 방식으로 실행할 수 있습니다.

### 1.1 웹 UI (Streamlit)에서 사용하기 [권장]
가장 직관적이고 편리한 방법입니다.

```powershell
# 프로젝트 루트 디렉토리에서 실행
streamlit run app/main.py
```
- 좌측 사이드바에서 **'Agent Chat'**을 선택합니다.
- 채팅창에 원하는 작업을 지시하면 에이전트가 생각하는 과정과 도구 실행 결과를 실시간으로 보여줍니다.

### 1.2 CLI (터미널)에서 사용하기
개발 테스트나 스크립트 연동 시 유용합니다.

```powershell
# 프로젝트 루트 디렉토리에서 실행
python -m agent.core
```
- 프롬프트에 질문이나 지시를 입력합니다. (예: "현재 폴더의 파일 목록을 알려줘")
- 에이전트의 구체적인 사고 과정(Thought)과 도구 입력(Action Input), 결과(Observation)가 터미널에 상세히 출력됩니다.

### 💡 활용 예시
- **위키 통합 작업**: "비씨카드 연회비 관련 내용을 위키에서 검색하고, 그 내용을 요약해서 `bc_fee_summary.txt` 파일로 저장해줘."
- **파일/코드 작업**: "1부터 100까지의 소수를 구하는 파이썬 코드를 작성해서 실행하고, 그 결과를 알려줘."
- **시스템 확인**: "현재 디렉토리에서 `.py` 파일이 몇 개 있는지 셸 명령어로 확인해줘."

---

## 2. Agent 기능 추가하기 (새로운 Tool 만들기)

에이전트에게 새로운 기능을 부여하려면 새로운 `Tool` 클래스를 작성하여 등록하면 됩니다. (예: 사내 결재 시스템 API 연동 도구)

### 1단계: 도구 클래스 및 입력 스키마 작성
`agent/tools/` 디렉토리에 새로운 파이썬 파일(예: `api_tool.py`)을 생성합니다.

```python
# agent/tools/api_tool.py
import requests
from .base import Tool
from pydantic import BaseModel, Field

# 1. 인자 스키마 정의 (에이전트가 어떤 인자를 넘겨야 하는지 명세)
class ApprovalArgs(BaseModel):
    doc_id: str = Field(description="결재할 문서의 ID")

# 2. 도구 클래스 정의 (Tool 상속)
class ApprovalTool(Tool):
    name = "approve_document"                     # 도구의 고유 이름
    description = "지정된 ID의 문서를 사내 시스템에서 결재 처리합니다." # 에이전트가 읽을 설명
    args_schema = ApprovalArgs

    def run(self, doc_id: str) -> str:
        # 3. 실제 동작 로직 구현
        try:
            # 예시: 사내 API 호출
            response = requests.post(f"http://api.company.com/approve/{doc_id}")
            if response.status_code == 200:
                return f"{doc_id} 문서 결재가 완료되었습니다."
            else:
                return f"결재 실패: {response.text}"
        except Exception as e:
            return f"오류 발생: {str(e)}"
```

### 2단계: Agent Core에 도구 등록
작성한 도구를 에이전트가 사용할 수 있도록 `agent/core.py`에 등록합니다.

```python
# agent/core.py 수정

# ... 기존 임포트 ...
from .tools.api_tool import ApprovalTool  # 1. 새 도구 임포트

class LOAgent:
    # ... 생략 ...

    def _setup_tools(self):
        self.registry.register(FileReadTool())
        self.registry.register(FileWriteTool())
        self.registry.register(ShellTool())
        self.registry.register(WikiSearchTool())
        self.registry.register(PythonTool())
        
        # 2. 도구 레지스트리에 등록
        self.registry.register(ApprovalTool()) 
```

### 3단계: 테스트
에이전트를 실행하고 "12345번 문서를 결재해줘"라고 지시하면, 에이전트가 새롭게 등록된 `approve_document` 도구의 `description`을 읽고 알아서 해당 도구를 선택하여 실행합니다.

---

## 📌 기능 추가 시 핵심 팁
- **명확한 `description`**: 에이전트는 `description`을 읽고 도구를 언제 사용할지 판단합니다. **언제, 어떤 목적으로 이 도구를 써야 하는지** 상세히 적어주세요.
- **Pydantic 스키마**: `Field(description="...")`를 꼼꼼히 작성할수록 에이전트가 인자값을 정확하게 추출하여 넘겨줍니다.
- **예외 처리**: 도구 내부(`run` 메서드)에서 에러가 발생해도 프로그램이 뻗지 않고 에이전트가 다시 시도할 수 있도록, `try-except`로 묶어 에러 메시지를 `return` 해주는 것이 좋습니다.
