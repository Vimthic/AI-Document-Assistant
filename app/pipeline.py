from app.file_reader import read_text_file
from app.preprocessing import clean_text

def process_text_document(file_path):

    text = read_text_file(file_path)

    cleaned = clean_text(text)

    return cleaned