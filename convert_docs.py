import os
import argparse
from pathlib import Path
import fitz  # PyMuPDF
from docx import Document
import shutil

def convert_pdf_to_txt(pdf_path):
    """PDF 파일을 텍스트로 변환합니다."""
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"PDF 변환 오류 ({pdf_path}): {e}")
    return text

def convert_docx_to_txt(docx_path):
    """DOCX 파일을 텍스트로 변환합니다."""
    text = ""
    try:
        doc = Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"DOCX 변환 오류 ({docx_path}): {e}")
    return text

def process_directory(input_dir, output_dir):
    """디렉토리 내의 모든 문서를 텍스트로 변환하여 저장합니다."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for file_path in input_path.rglob("*"):
        if file_path.is_dir():
            continue

        relative_path = file_path.relative_to(input_path)
        target_file = output_path / relative_path.with_suffix(".txt")
        target_file.parent.mkdir(parents=True, exist_ok=True)

        if file_path.suffix.lower() == ".pdf":
            print(f"변환 중 (PDF): {file_path.name}")
            content = convert_pdf_to_txt(file_path)
            if content:
                target_file.write_text(content, encoding="utf-8")
        
        elif file_path.suffix.lower() == ".docx":
            print(f"변환 중 (DOCX): {file_path.name}")
            content = convert_docx_to_txt(file_path)
            if content:
                target_file.write_text(content, encoding="utf-8")
        
        elif file_path.suffix.lower() in [".txt", ".md"]:
            print(f"복사 중: {file_path.name}")
            shutil.copy2(file_path, target_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="문서(PDF, DOCX)를 TXT로 변환합니다.")
    parser.add_argument("--input", required=True, help="입력 디렉토리")
    parser.add_argument("--output", required=True, help="출력 디렉토리 (kb/raw/ 권장)")
    
    args = parser.parse_args()
    process_directory(args.input, args.output)
