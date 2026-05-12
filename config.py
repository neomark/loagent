import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import httpx

# 환경 변수 로드
load_dotenv()

def get_llm(temperature=0.7, max_tokens=4096):
    """
    사내 로컬 LLM(bcgpt-27b) 인스턴스를 반환합니다.
    SSL 검증을 우회하도록 설정되어 있습니다.
    """
    base_url = os.getenv("LLM_BASE_URL", "URL")
    api_key = os.getenv("LLM_API_KEY", "TEST")
    model_name = os.getenv("LLM_MODEL", "bcgpt-27b")
    
    # SSL 검증 비활성화를 위한 클라이언트 설정
    http_client = httpx.Client(verify=False)
    
    return ChatOpenAI(
        model_name=model_name,
        base_url=base_url,
        api_key=api_key,
        http_client=http_client,
        temperature=temperature,
        max_tokens=max_tokens,
    )

def get_embedding_config():
    """
    임베딩 설정을 반환합니다.
    """
    return {
        "model": os.getenv("EMBEDDING_MODEL", "bge-m3"),
        "base_url": os.getenv("LLM_BASE_URL", "URL"),
        "api_key": os.getenv("LLM_API_KEY", "TEST"),
    }
