import streamlit as st

st.set_page_config(
    page_title="LOAgent & Wiki",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("LOAgent 통합 대시보드 🤖")

st.markdown("""
### 사내 로컬 LLM 기반 자동화 및 지식 관리 시스템

왼쪽 사이드바에서 원하는 기능을 선택하세요.

1. **📚 Wiki Viewer**: OpenKB 기반 사내 지식 베이스 열람 및 검색
2. **💬 Agent Chat**: LOAgent와 대화하며 다양한 자동화 작업 수행 (위키 검색, 파일 처리, 코드 실행 등)
3. **👨‍💻 Coding Chat**: LOCoder로 소스 코드 분석, 편집, 테스트를 자동 수행

---
#### 현재 시스템 상태
- **LLM**: bcgpt-27b (Local)
- **Embedding**: bge-m3
- **Wiki Path**: `./kb/wiki`
""")
