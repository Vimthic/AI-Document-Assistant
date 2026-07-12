from app.vector_store import VectorStore
from app.embeddings import generate_embedding

class Retriever:

    def __init__(self):
        # 1. Generate a dummy embedding to find the actual dimension size dynamically
        sample_embedding = generate_embedding("test")
        actual_dimension = len(sample_embedding)
        
        # 2. Pass the correct dimension to your VectorStore
        self.store = VectorStore(
            dimension=actual_dimension
        )

    def add_document(self, text):

        embedding = generate_embedding(text)

        self.store.add(
            embedding,
            text
        )

    def search(self, question):

        embedding = generate_embedding(
            question
        )

        return self.store.search(
            embedding
        )
