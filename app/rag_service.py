'''
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
        '''
from app.retriever import Retriever
from app.gemini_client import ask_gemini
from app.prompt_templates import build_rag_prompt
from app.memory import ConversationMemory

class RAGService:
    def __init__(self):
        self.retriever = Retriever()
        # Initialize memory framework with limited tracking boundaries
        self.memory = ConversationMemory(max_history_turns=4)

    def ask(self, question: str, chat_history_logs: list = None):
        """Processes questions, builds contexts, extracts source labels, and executes models."""
        # 1. Fetch matching documentation structures (Now dictionary objects)
        matched_chunks = self.retriever.search(question)
        
        # 2. Task 3: Build Context Blocks separated by clear Source fields
        formatted_context_segments = []
        for idx, item in enumerate(matched_chunks):
            # Safe recovery handling if older data contains raw strings instead of dictionaries
            if isinstance(item, dict):
                text_content = item.get("text", "")
                fname = item.get("filename", "Unknown Document")
                chunk_num = item.get("chunk_number", idx + 1)
            else:
                text_content = str(item)
                fname = "Legacy_Document_Dump.txt"
                chunk_num = idx + 1
                
            segment = f"Source:\n{fname} (Chunk #{chunk_num})\n{text_content}"
            formatted_context_segments.append(segment)
            
        full_context_payload = "\n\n".join(formatted_context_segments)
        
        # 3. Format lookback transaction items via your memory engine
        history_buffer = self.memory.get_formatted_history(chat_history_logs or [])
        
        # 4. Synthesize your final enterprise prompt using isolated layouts
        final_prompt = build_rag_prompt(
            context=full_context_payload,
            history=history_buffer,
            question=question
        )
        
        # 5. Route prompt straight through to your stable Gemini streaming interface
        return ask_gemini(final_prompt)
