from app.pipeline import process_text_document
from app.gemini_client import ask_gemini

def summarize_document(path):

    document = process_text_document(path)

    prompt = f"""
    Extract only leave policy.

    {document}
    """

    return ask_gemini(prompt)