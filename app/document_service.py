from app.pipeline import process_text_document
from app.gemini_client import ask_gemini

def summarize_document(path):

    document = process_text_document(path)

    prompt = f"""
    Summarize the document.

    {document}
    """

    return ask_gemini(prompt)

def explain_document(path):

    document = process_text_document(path)

    prompt = f"""
    Explain this policy like I'm a new employee

    {document}
    """

    return ask_gemini(prompt)