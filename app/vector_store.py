'''
import faiss
import numpy as np

class VectorStore:

    def __init__(self, dimension):

        self.index = faiss.IndexFlatL2(dimension)

        self.documents = []

    def add(self, embedding, text):

        vector = np.array(
            [embedding],
            dtype="float32"
        )

        self.index.add(vector)

        self.documents.append(text)

    def search(self, embedding, k=3):

        vector = np.array(
            [embedding],
            dtype="float32"
        )

        distances, indexes = self.index.search(
            vector,
            k
        )

        results = []

        for idx in indexes[0]:

            if idx != -1:
                results.append(
                    self.documents[idx]
                )

        return results
    
    def save(self, path):
        faiss.write_index(
            self.index,
            str(path)
        )
        
    def load(self, path):
        self.index = faiss.read_index(
            str(path)
        )
 '''

 #for FAISS index store
import os
import faiss
import numpy as np
from app.metadata_store import save_documents, load_documents

class VectorStore:

    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []

    def add(self, embedding, text):
        vector = np.array(
            [embedding],
            dtype="float32"
        )
        self.index.add(vector)
        self.documents.append(text)

    def search(self, embedding, k=3):
        vector = np.array(
            [embedding],
            dtype="float32"
        )

        # FIX: Ensure k never exceeds the actual number of documents indexed
        actual_k = min(k, len(self.documents))
        if actual_k == 0:
            return []

        distances, indexes = self.index.search(
            vector,
            actual_k
        )

        results = []
        # Accessing indexes[0] handles the top matches array securely
        for idx in indexes[0]:
            # FIX: Prevent out-of-bounds mapping errors
            if idx != -1 and idx < len(self.documents):
                results.append(
                    self.documents[idx]
                )

        return results
    
    def save(self, faiss_path, metadata_path):
        """Saves the numerical index and text metadata to their respective folders."""
        # 1. Save the numerical FAISS index matrix to storage/faiss/
        faiss.write_index(
            self.index,
            f"{faiss_path}.index"
        )
        # 2. Save the matching text chunks to storage/metadata/
        save_documents(
            f"{metadata_path}.json", 
            self.documents
        )
        
    def load(self, faiss_path, metadata_path):
        """Loads the numerical index and text metadata from their respective folders."""
        # 1. Load the numerical FAISS matrix from storage/faiss/
        self.index = faiss.read_index(
            f"{faiss_path}.index"
        )
        # 2. Restore the matching text chunks into memory from storage/metadata/
        self.documents = load_documents(
            f"{metadata_path}.json"
        )
