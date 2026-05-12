import os
from config import get_llm, get_embedding_config
from openai import OpenAI
import httpx

def test_llm_connection():
    print("--- LLM 연결 테스트 시작 ---")
    try:
        llm = get_llm()
        messages = [
            {"role": "system", "content": "한국말로만 응답주세요"},
            {"role": "user", "content": "비씨카드에 대해 간단히 알려줘"}
        ]
        response = llm.invoke(messages)
        print("응답 성공:")
        print(response.content)
    except Exception as e:
        print(f"LLM 연결 실패: {e}")

def test_embedding_connection():
    print("\n--- 임베딩 연결 테스트 시작 ---")
    config = get_embedding_config()
    try:
        # OpenAI SDK를 사용한 직접 호출 테스트
        client = OpenAI(
            base_url=config["base_url"],
            api_key=config["api_key"],
            http_client=httpx.Client(verify=False)
        )
        
        texts = ["안녕하세요", "비씨카드 테스트입니다"]
        response = client.embeddings.create(
            model=config["model"],
            input=texts
        )
        print(f"임베딩 성공: {len(response.data)} 개의 벡터 생성됨")
        print(f"벡터 차원: {len(response.data[0].embedding)}")
    except Exception as e:
        print(f"임베딩 연결 실패: {e}")

if __name__ == "__main__":
    test_llm_connection()
    test_embedding_connection()
