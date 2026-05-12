import streamlit as st
import sys
import os

# Agent 코어 모듈 경로 추가
sys.path.append(os.getcwd())
from agent.coding_agent import CodingAgent

st.set_page_config(page_title="LOCoder", page_icon="👨‍💻", layout="wide")
st.title("👨‍💻 LOCoder - 코딩 에이전트")

st.markdown("""
> 소스 코드 분석, 편집, 테스트를 자동 수행하는 코딩 전문 에이전트입니다.
> 코드를 읽고, 수정하고, 테스트까지 자동으로 처리합니다.
""")

# 작업 디렉토리 설정
work_dir = st.sidebar.text_input("📂 작업 디렉토리", value=os.getcwd())
if st.sidebar.button("디렉토리 변경"):
    if os.path.exists(work_dir):
        os.chdir(work_dir)
        st.sidebar.success(f"변경됨: {work_dir}")
    else:
        st.sidebar.error("존재하지 않는 경로입니다.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 사용 가능한 도구")
st.sidebar.markdown("""
- `code_read` — 코드 읽기 (라인 번호 포함)
- `code_edit` — 코드 편집 (라인 범위 치환)
- `code_insert` — 코드 삽입
- `code_search` — 패턴 검색
- `list_files` — 파일 목록 조회
- `test_run` — pytest 실행
- `script_run` — 스크립트 실행
- `git_command` — Git 명령
- `file_read` / `file_write`
""")

# 세션 상태 초기화
if "coding_agent" not in st.session_state:
    with st.spinner("LOCoder 초기화 중..."):
        try:
            st.session_state.coding_agent = CodingAgent()
        except Exception as e:
            st.error(f"초기화 오류: {e}")

if "coding_messages" not in st.session_state:
    st.session_state.coding_messages = []

# 이전 채팅 이력 출력
for message in st.session_state.coding_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("코딩 작업을 요청하세요 (예: config.py의 get_llm 함수에 타임아웃 인자를 추가해줘)"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.coding_messages.append({"role": "user", "content": prompt})

    if "coding_agent" in st.session_state:
        with st.chat_message("assistant"):
            with st.spinner("LOCoder가 코드를 분석하고 작업 중입니다..."):
                try:
                    response = st.session_state.coding_agent.run(prompt)
                    st.markdown(response)
                    st.session_state.coding_messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"실행 중 오류 발생: {e}"
                    st.error(error_msg)
                    st.session_state.coding_messages.append({"role": "assistant", "content": error_msg})
    else:
        st.error("CodingAgent가 정상적으로 초기화되지 않았습니다.")
