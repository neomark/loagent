import streamlit as st
import os
import subprocess

st.set_page_config(page_title="Wiki Viewer", page_icon="📚", layout="wide")
st.title("📚 사내 지식 베이스 (Wiki)")

# 위키 디렉토리 설정
WIKI_DIR = os.path.join(os.getcwd(), "kb", "wiki")

# 탭 구성: 열람, 검색, QA
tab1, tab2 = st.tabs(["📄 문서 열람", "🔍 위키 검색 및 QA"])

with tab1:
    st.header("문서 탐색기")
    
    if not os.path.exists(WIKI_DIR):
        st.warning(f"위키 디렉토리가 존재하지 않습니다: {WIKI_DIR}\n먼저 위키를 초기화해주세요.")
    else:
        # 카테고리 선택 (디렉토리 기준)
        categories = ["전체"] + [d for d in os.listdir(WIKI_DIR) if os.path.isdir(os.path.join(WIKI_DIR, d)) and not d.startswith('.')]
        selected_category = st.selectbox("카테고리 선택", categories)
        
        # 파일 목록 가져오기
        files = []
        if selected_category == "전체":
            for root, _, filenames in os.walk(WIKI_DIR):
                for filename in filenames:
                    if filename.endswith(".md"):
                        files.append(os.path.relpath(os.path.join(root, filename), WIKI_DIR))
        else:
            cat_dir = os.path.join(WIKI_DIR, selected_category)
            for filename in os.listdir(cat_dir):
                if filename.endswith(".md"):
                    files.append(os.path.join(selected_category, filename))
        
        if not files:
            st.info("선택한 카테고리에 마크다운 파일이 없습니다.")
        else:
            selected_file = st.selectbox("파일 선택", files)
            file_path = os.path.join(WIKI_DIR, selected_file)
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            st.markdown("---")
            st.markdown(content)

with tab2:
    st.header("OpenKB 질의응답")
    query = st.text_input("질문이나 검색어를 입력하세요:")
    
    if st.button("검색/질문"):
        if query:
            with st.spinner("위키 검색 중..."):
                kb_dir = os.path.join(os.getcwd(), "kb")
                try:
                    # openkb query 명령 실행
                    result = subprocess.run(
                        f"openkb query \"{query}\"",
                        shell=True,
                        cwd=kb_dir,
                        capture_output=True,
                        text=True,
                        env={**os.environ, "PYTHONIOENCODING": "utf-8"}
                    )
                    
                    if result.returncode != 0:
                        st.error(f"검색 오류:\n{result.stderr}")
                    else:
                        st.markdown("### 결과")
                        st.markdown(result.stdout)
                except Exception as e:
                    st.error(f"실행 중 예외 발생: {str(e)}")
        else:
            st.warning("검색어를 입력해주세요.")
