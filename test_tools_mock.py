import os
from agent.tools.file_tool import FileWriteTool, FileReadTool
from agent.tools.code_read_tool import CodeReadTool
from agent.tools.code_edit_tool import CodeEditTool
from agent.tools.code_search_tool import CodeSearchTool
from agent.tools.test_run_tool import ScriptRunTool

def test_core_tools():
    print("=== LOAgent/LOCoder 도구 독립 테스트 ===\n")

    # 1. 파일 쓰기 테스트
    print("[1] FileWriteTool 테스트")
    write_tool = FileWriteTool()
    write_result = write_tool.run(file_path="test_mock.txt", content="Hello, LOAgent!\nThis is line 2.\nThis is line 3.")
    print(f"결과: {write_result}\n")

    # 2. 파일 읽기 (코드용) 테스트
    print("[2] CodeReadTool 테스트")
    read_tool = CodeReadTool()
    read_result = read_tool.run(file_path="test_mock.txt")
    print("결과:")
    print(read_result)
    print()

    # 3. 코드 편집 테스트
    print("[3] CodeEditTool 테스트 (2번째 줄 수정)")
    edit_tool = CodeEditTool()
    edit_result = edit_tool.run(
        file_path="test_mock.txt", 
        start_line=2, 
        end_line=2, 
        new_content="This line was edited by CodeEditTool!"
    )
    print(f"결과: {edit_result}\n")

    print("수정된 파일 내용 확인:")
    print(read_tool.run(file_path="test_mock.txt"))
    print()

    # 4. 코드 검색 테스트
    print("[4] CodeSearchTool 테스트 ('edited' 검색)")
    search_tool = CodeSearchTool()
    search_result = search_tool.run(pattern="edited", directory=".", file_ext="test_mock.txt")
    print("결과:")
    print(search_result)
    print()

    # 5. 스크립트 실행 테스트 (간단한 파이썬 코드 생성 및 실행)
    print("[5] ScriptRunTool 테스트")
    write_tool.run(file_path="hello.py", content="print('Hello from executed script!')")
    script_tool = ScriptRunTool()
    script_result = script_tool.run(script_path="hello.py")
    print("결과:")
    print(script_result)
    print()

    # 정리
    os.remove("test_mock.txt")
    os.remove("hello.py")
    print("테스트 완료 및 임시 파일 정리됨.")

if __name__ == "__main__":
    test_core_tools()
