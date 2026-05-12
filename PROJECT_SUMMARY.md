# LOAgent 프로젝트 요약

## 프로젝트 개요
사내 로컬 LLM(bcgpt-27b)을 활용한 3가지 시스템 구축 프로젝트

### 1. LLM Wiki 시스템 (OpenKB 기반)
- OpenKB 라이브러리를 활용하여 사내 문서를 마크다운 위키로 자동 변환
- PageIndex 트리 인덱싱으로 벡터DB 없이 검색/질의응답 지원
- DRM 문서 → TXT 변환 → raw/ 투입 → 위키 자동 생성
- Obsidian 호환 마크다운 위키

### 2. LOAgent (OpenClaw 유사 Agent)
- ReAct 패턴 기반 자동화 Agent
- Tool/Skill 기반 확장 가능한 아키텍처 (파일, 셸, HTTP, Python, 위키검색)
- 마크다운 기반 스킬 시스템

### 3. LOCoder (코딩 에이전트)
- 소스 코드 분석, 편집, 테스트를 자동 수행하는 코딩 전용 Agent
- 코드 읽기/편집/삽입, 패턴 검색, pytest 실행, Git 관리 도구 탑재
- ReAct 패턴 기반 (코드 확인 → 수정 → 테스트 → 재수정 자동 루프)

### 4. Streamlit 통합 UI
- 위키 뷰어/검색/QA + Agent 채팅 + 코딩 에이전트 통합 인터페이스

## 기술 환경
- **언어**: Python 3.11
- **패키지 관리**: pip (Nexus 프록시 경유, uv 사용 불가)
- **LLM**: bcgpt-27b (OpenAI 호환 API, httpx verify=False)
- **임베딩**: bge-m3 (동일 API 서버)
- **Wiki**: OpenKB + LiteLLM
- **네트워크**: 인터넷 차단, Nexus를 통한 라이브러리만 사용 가능

## 개발 로드맵 (4 Phase, 5주)
- Phase 1 (1.5주): OpenKB 기반 LLM Wiki 구축
- Phase 2 (1.5주): LOAgent 자동화 Agent 구축
- Phase 3 (1주): Streamlit 통합 UI + 연동/테스트
- Phase 4 (1주): LOCoder 코딩 에이전트 추가

## 현재 상태
- 📅 시작일: 2026-05-12
- 📌 단계: Phase 4 완료
- ✅ 완료 항목:
    - Phase 1: OpenKB 기반 지식 베이스 및 문서 변환 파이프라인
    - Phase 2: LOAgent 코어 및 다양한 확장 도구(Tool) 구현
    - Phase 3: Streamlit 기반 통합 대시보드(Wiki Viewer, Agent Chat) 구축
    - Phase 4: LOCoder 코딩 에이전트 (코드 편집/테스트/Git 도구 7종 + 전용 UI)

## 🛠️ 작업 재개 및 테스트 가이드

### 1. 환경 설정 (최초 실행 시)
- `.env` 및 `kb/.env` 파일의 `LLM_BASE_URL`을 실제 사내 URL로 수정하십시오.
- `pip install -r requirements.txt`로 의존성을 설치하십시오.

### 2. 위키 구축
- DRM 해제된 문서를 특정 폴더에 넣고 `python convert_docs.py --input [폴더] --output ./kb/raw/` 실행
- `cd kb; $env:PYTHONIOENCODING='utf-8'; openkb add raw/` 실행하여 지식 베이스 구축

### 3. 시스템 실행
- **통합 UI**: `streamlit run app/main.py`
- **에이전트 단독 (CLI)**: `python -m agent.core` 또는 `python -m agent.coding_agent`

### 4. 기능 검증
- LLM 연결 전 도구 로직 확인: `python test_tools_mock.py` 실행
- LLM 연결 상태 확인: `python test_connection.py` 실행

## 🔗 주요 문서
- [README.md](README.md): 전체 시스템 설치 및 실행 가이드
- [AGENT_GUIDE.md](AGENT_GUIDE.md): LOAgent 및 LOCoder 사용법, 도구 추가 방법
- [test_tools_mock.py](test_tools_mock.py): LLM 없이 도구 단독 작동 여부 검증 스크립트
