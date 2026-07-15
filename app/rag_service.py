from app.retriever import Retriever
from app.gemini_client import ask_gemini

class RAGService:

    def __init__(self):
        self.retriever = Retriever()

    def load_documents(self, documents):

        for document in documents:
            self.retriever.add_document(document)

    def ask(self, question):

        chunks = self.retriever.search(question)
        # If search returns a list of dictionaries, extract the text strings first
        #context = "\n\n".join([item["text"] for item in chunks])

        context = "\n\n".join(chunks)

        prompt = f"""
You are an HR assistant.

Answer ONLY from the provided context.

If the answer is not found in the context,

DO NOT guess.

Reply:

"I couldn't find that information in the uploaded documents."

Context:

{context}

Question:

{question}
"""

        return ask_gemini(prompt)