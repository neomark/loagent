# LOAgent 시스템 설치 및 실행 가이드

본 문서는 사내 로컬 LLM을 활용한 **LLM Wiki (OpenKB)** 및 **LOAgent (자동화 에이전트)** 통합 시스템의 설치부터 실행까지의 과정을 안내합니다.

---

## 1. 사전 준비 (Prerequisites)

- **Python**: 3.11 버전 권장 (최소 3.10 이상)
- **네트워크**: 사내망 (인터넷 차단, Nexus 프록시 사용)
- **로컬 LLM**: 사내 서버(bcgpt-27b)의 API 엔드포인트 URL 및 API Key (OpenAI 호환 포맷 지원)
- **문서**: 지식 베이스로 활용할 사내 문서 (PDF, DOCX). *단, DRM이 걸려있는 문서는 사전에 DRM 해제가 필요합니다.*

---

## 2. 설치 (Installation)

### 2.1 패키지 설치
사내 Nexus 프록시 환경에서 `pip`를 사용하여 필요한 패키지들을 설치합니다. (uv는 사용 불가)

```powershell
# 프로젝트 루트 디렉토리(d:\workspace\loagent)에서 실행
pip install -r requirements.txt
```

### 2.2 환경변수 설정
프로젝트 루트 폴더와 `kb` 폴더에 각각 환경변수 파일(`.env`)을 설정해야 합니다.

1. **루트 디렉토리 (`d:\workspace\loagent\.env`)**
   `.env.example` 파일을 복사하여 `.env`를 생성하고, `URL` 부분을 **실제 LLM 엔드포인트 주소**로 변경합니다.

   ```env
   # LLM 설정
   LLM_BASE_URL=http://your-llm-server:port/v1  # 실제 주소로 변경
   LLM_API_KEY=TEST
   LLM_MODEL=bcgpt-27b
   
   # 임베딩 설정
   EMBEDDING_MODEL=bge-m3
   
   # OpenKB용 LiteLLM 설정
   OPENAI_API_BASE=http://your-llm-server:port/v1 # 실제 주소로 변경
   OPENAI_API_KEY=TEST
   
   # SSL 검증 우회 (사내망 인증서 문제 방지)
   CURL_CA_BUNDLE=""
   HTTPX_VERIFY=False
   ```

2. **지식 베이스 디렉토리 (`d:\workspace\loagent\kb\.env`)**
   이곳에도 동일하게 LiteLLM 접속을 위한 `.env`를 구성해야 합니다.

   ```env
   OPENAI_API_KEY=TEST
   OPENAI_API_BASE=http://your-llm-server:port/v1 # 실제 주소로 변경
   SSL_CERT_FILE=""
   CURL_CA_BUNDLE=""
   ```

### 2.3 LLM 연결 테스트
설정이 올바른지 스크립트를 실행하여 확인합니다.

```powershell
python test_connection.py
```
*(정상 시 "응답 성공" 및 "임베딩 성공" 메시지가 출력되어야 합니다.)*

---

## 3. 지식 베이스 (Wiki) 구축하기

### 3.1 문서 변환 (DRM 해제 문서 대상)
PDF나 DOCX 파일을 OpenKB가 쉽게 처리할 수 있도록 TXT 파일로 변환합니다.

```powershell
# 원본 문서가 ./documents 폴더에 있다고 가정할 때
python convert_docs.py --input ./documents --output ./kb/raw/
```
*(`kb/raw/` 경로에 텍스트 파일들이 저장됩니다.)*

### 3.2 위키 생성 (Knowledge Compilation)
로컬 LLM이 변환된 문서를 읽고 구조화된 마크다운 위키(요약, 개념 정리, 상호 링크 등)를 자동으로 생성합니다.

```powershell
cd kb
# Windows 인코딩 에러 방지 및 위키 구축 실행
$env:PYTHONIOENCODING='utf-8'; openkb add raw/
```
*(수행 완료 시 `kb/wiki` 폴더에 `.md` 파일들이 생성됩니다.)*

---

## 4. 시스템 실행 (Execution)

지식 베이스 구축이 완료되면, Streamlit을 활용한 통합 웹 UI를 실행하여 시스템을 사용합니다.

```powershell
# 다시 프로젝트 루트 디렉토리로 이동
cd d:\workspace\loagent

# Streamlit 대시보드 실행
streamlit run app/main.py
```

명령어를 실행하면 웹 브라우저가 열리며(기본 `http://localhost:8501`), 아래 두 가지 주요 기능을 사용할 수 있습니다.

1. **Wiki Viewer**: 구축된 지식 베이스를 열람하고, `openkb query` 기반의 질의응답(RAG)을 수행합니다.
2. **Agent Chat**: LOAgent와 대화하며, 에이전트가 스스로 파일을 분석하거나, 위키를 검색하거나, 터미널 명령을 실행하여 복잡한 업무를 대신 처리하도록 지시할 수 있습니다.
3. **Coding Chat**: 코딩 전문 에이전트(LOCoder)를 통해 소스 코드 분석, 수정, 테스트를 자동화할 수 있습니다.
