import json

def save_documents(path, docs):
    # Added encoding="utf-8" to handle special characters safely
    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            docs,
            file,
            indent=2,
            ensure_ascii=False  # Ensures non-English text displays correctly in the file
        )

def load_documents(path):
    # Added encoding="utf-8" to match the save configuration
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)
