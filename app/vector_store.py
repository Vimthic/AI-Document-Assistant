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
 
# worked till aug 6
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
'''
# app/vector_store.py
import os
import faiss
import numpy as np
from app.metadata_store import save_documents, load_documents

class VectorStore:
    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []

    def add(self, embedding, text_dict):
        vector = np.array([embedding], dtype="float32")
        self.index.add(vector)
        self.documents.append(text_dict)

    def search(self, embedding, k=3, category_filter="All"):
        vector = np.array([embedding], dtype="float32")
        if len(self.documents) == 0:
            return []

        search_k = min(k * 5 if category_filter != "All" else k, len(self.documents))
        distances, indexes = self.index.search(vector, search_k)

        results = []
        if len(indexes) > 0:
            for dist, idx in zip(distances[0], indexes[0]):
                if idx != -1 and idx < len(self.documents):
                    doc_payload = self.documents[idx]
                    category = doc_payload.get("category", "HR")
                    
                    if category_filter != "All" and category != category_filter:
                        continue
                    
                    # Distance Score Normalization Formula
                    normalized_score = round(1.0 / (1.0 + float(dist)), 2)
                    
                    results.append({
                        "text": doc_payload.get("text", ""),
                        "score": normalized_score,
                        "filename": doc_payload.get("filename", "Unknown"),
                        "category": category,
                        "chunk_number": doc_payload.get("chunk_number", 1)
                    })
                    if len(results) == k:
                        break
        return results
    
    def save(self, faiss_path, metadata_path):
        faiss.write_index(self.index, f"{faiss_path}.index")
        save_documents(f"{metadata_path}.json", self.documents)
        
    def load(self, faiss_path, metadata_path):
        self.index = faiss.read_index(f"{faiss_path}.index")
        self.documents = load_documents(f"{metadata_path}.json")
