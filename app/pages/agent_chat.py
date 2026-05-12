import streamlit as st
import sys
import os

# Agent 코어 모듈 경로 추가
sys.path.append(os.getcwd())
from agent.core import LOAgent

st.set_page_config(page_title="LOAgent Chat", page_icon="💬", layout="wide")
st.title("💬 LOAgent 채팅")

# 세션 상태에 Agent 인스턴스 저장 (최초 1회 생성)
if "agent" not in st.session_state:
    with st.spinner("LOAgent 초기화 중..."):
        try:
            st.session_state.agent = LOAgent()
        except Exception as e:
            st.error(f"Agent 초기화 오류: {e}")

# 채팅 이력 초기화 (Streamlit UI용)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 채팅 이력 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("LOAgent에게 작업을 요청하세요 (예: 특정 파일 내용 요약, 위키 검색 후 파일 저장 등)"):
    # 사용자 메시지 UI 추가
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Agent 응답 생성
    if "agent" in st.session_state:
        with st.chat_message("assistant"):
            with st.spinner("LOAgent가 생각 중입니다... (여러 도구를 사용할 수 있습니다)"):
                try:
                    # Agent 실행 (내부적으로 ReAct 루프 동작)
                    response = st.session_state.agent.run(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"실행 중 오류 발생: {e}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    else:
        st.error("Agent가 정상적으로 초기화되지 않았습니다. 설정을 확인해주세요.")
