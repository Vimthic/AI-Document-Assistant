from pathlib import Path

def read_text_file(file_path):
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        return file.read()