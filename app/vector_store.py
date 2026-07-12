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