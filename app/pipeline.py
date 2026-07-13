'''
from app.file_reader import read_text_file
from app.preprocessing import clean_text

def process_text_document(file_path):

    text = read_text_file(file_path)

    cleaned = clean_text(text)

    return cleaned
 '''

from app.file_reader import read_text_file
from app.preprocessing import clean_text
from app.chunking import split_document

def process_text_document(file_path):
    # 1. Read raw text (keeps \n and original structure)
    raw_text = read_text_file(file_path)

    # 2. Let LangChain split the raw text into smart chunks
    raw_chunks = split_document(raw_text)

    # 3. Clean each chunk individually
    cleaned_chunks = []
    for chunk in raw_chunks:
        cleaned = clean_text(chunk)
        if cleaned:
            cleaned_chunks.append(cleaned)

    return cleaned_chunks
