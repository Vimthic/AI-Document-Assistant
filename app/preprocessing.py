import re

def clean_text(text):
    text = text.lower()
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s.]", "", text)
    return text.strip()