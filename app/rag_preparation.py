'''from app.pipeline import process_text_document
from app.chunking import split_document
from app.embeddings import generate_embedding

def prepare_document(path):

    text = process_text_document(path)

    chunks = split_document(text)

    vectors = []

    for chunk in chunks:

        embedding = generate_embedding(chunk)

        vectors.append(
            {
                "text": chunk,
                "embedding": embedding,
            }
        )

    return vectors
    '''

# app/rag_preparation.py

# 1. Import your Retriever class
from app.retriever import Retriever

def prepare_rag_system(documents_list):
    """
    Takes a list of raw documents/texts, chunks them, 
    and inserts them directly into the vector database.
    """
    # 2. Initialize your Retriever 
    # (This will automatically detect the dimension using our previous fix!)
    retriever = Retriever()
    
    print("Starting document ingestion into Vector Store...")

    for doc in documents_list:
        # 3. Chunking Logic (Break large texts into smaller, readable paragraphs)
        chunks = chunk_text(doc, chunk_size=500, overlap=50)
        
        for chunk in chunks:
            # 4. Storage Logic
            # Calling add_document will internally generate the embedding 
            # and append the text chunk into your FAISS index simultaneously.
            retriever.add_document(chunk)
            
    print(f"Ingestion complete! All chunks securely stored locally.")
    return retriever


def chunk_text(text, chunk_size=500, overlap=50):
    """
    A simple helper function to slice text into overlapping chunks 
    so context isn't lost at the edges of sentences.
    """
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)
        
    return chunks
