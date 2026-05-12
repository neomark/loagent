# LOAgent 프로젝트 요약

## 프로젝트 개요
사내 로컬 LLM(bcgpt-27b)을 활용한 2가지 시스템 구축 프로젝트

### 1. LLM Wiki 시스템 (OpenKB 기반)
- OpenKB 라이브러리를 활용하여 사내 문서를 마크다운 위키로 자동 변환
- PageIndex 트리 인덱싱으로 벡터DB 없이 검색/질의응답 지원
- DRM 문서 → TXT 변환 → raw/ 투입 → 위키 자동 생성
- Obsidian 호환 마크다운 위키

### 2. LOAgent (OpenClaw 유사 Agent)
- ReAct 패턴 기반 자동화 Agent
- Tool/Skill 기반 확장 가능한 아키텍처 (파일, 셸, HTTP, Python, 위키검색)
- 마크다운 기반 스킬 시스템

### 3. Streamlit 통합 UI
- 위키 뷰어/검색/QA + Agent 채팅 통합 인터페이스

## 기술 환경
- **언어**: Python 3.11
- **패키지 관리**: pip (Nexus 프록시 경유, uv 사용 불가)
- **LLM**: bcgpt-27b (OpenAI 호환 API, httpx verify=False)
- **임베딩**: bge-m3 (동일 API 서버)
- **Wiki**: OpenKB + LiteLLM
- **네트워크**: 인터넷 차단, Nexus를 통한 라이브러리만 사용 가능

## 개발 로드맵 (3 Phase, 4주)
- Phase 1 (1.5주): OpenKB 기반 LLM Wiki 구축
- Phase 2 (1.5주): LOAgent 자동화 Agent 구축
- Phase 3 (1주): Streamlit 통합 UI + 연동/테스트

## 현재 상태
- 📅 시작일: 2026-05-12
- 📌 단계: Phase 3 완료 (통합 UI 구축 및 전체 프로젝트 완료)
- ✅ 완료 항목:
    - Phase 1: OpenKB 기반 지식 베이스 및 문서 변환 파이프라인
    - Phase 2: LOAgent 코어 및 다양한 확장 도구(Tool) 구현
    - Phase 3: Streamlit 기반 통합 대시보드(Wiki Viewer, Agent Chat) 구축
