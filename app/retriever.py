'''
from app.vector_store import VectorStore
from app.embeddings import generate_embedding
from app.rag_preparation import prepare_document

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
    
    def index_document(self, file_path):

        chunks = prepare_document(file_path)

        for item in chunks:

            self.store.add(
                item["embedding"],
                item["text"]
            )

#for aug 5 test            
import os
from app.vector_store import VectorStore
from app.embeddings import generate_embedding
from app.rag_preparation import prepare_document
from app.logger import log_secure_action, log_milestone

# Storage path setups matching your VectorStore's extension expectations (.index and .json)
FAISS_PATH = "storage/faiss/faiss_store"
METADATA_PATH = "storage/metadata/faiss_store"

class Retriever:
    def __init__(self):
        # Start with None. We will build the VectorStore dynamically when data arrives.
        self.store = None
        
        # Internal UI metrics state trackers
        self.total_chunks = 0
        self.indexed_files_list = set()

    def add_document(self, text):
        embedding = generate_embedding(text)
        if self.store is None:
            actual_dimension = len(embedding)
            self.store = VectorStore(dimension=actual_dimension)
        self.store.add(embedding, text)

    def search(self, question):
        log_secure_action("search", file_name="", count=3)
        embedding = generate_embedding(str(question))
        if self.store is None:
            return []
        return self.store.search(embedding)

    def index_document(self, file_path):
        file_path = str(file_path)
        filename = os.path.basename(file_path)
        
        chunks = prepare_document(file_path)
        
        for item in chunks:
            emb = item.get("embedding") if "embedding" in item else generate_embedding(item["text"])
            
            # FIXED PERMANENTLY: If the store doesn't exist yet, inspect the incoming 
            # vector length from Google and initialize the VectorStore to match it perfectly!
            if self.store is None:
                actual_dimension = len(emb)
                self.store = VectorStore(dimension=actual_dimension)
            
            # Pass the raw embedding directly to your original VectorStore
            self.store.add(emb, item["text"])
            
        # Update metrics tracking securely
        self.total_chunks += len(chunks)
        self.indexed_files_list.add(filename)
        log_secure_action("index_file", file_name=file_path, count=len(chunks))

    def build_index(self, upload_dir):
        self.total_chunks = 0
        self.indexed_files_list.clear()
        
        if not os.path.exists(upload_dir):
            return []
            
        existing_files = [f for f in os.listdir(upload_dir) if f.endswith(('.txt', '.csv'))]
        for existing_file in existing_files:
            file_path = os.path.join(upload_dir, existing_file)
            try:
                self.index_document(file_path)
            except Exception as e:
                print(f"Error pre-indexing {existing_file}: {e}")
                
        if self.store is not None and len(self.store.documents) > 0:
            os.makedirs(os.path.dirname(FAISS_PATH), exist_ok=True)
            os.makedirs(os.path.dirname(METADATA_PATH), exist_ok=True)
            self.store.save(FAISS_PATH, METADATA_PATH)
            log_secure_action("create", file_name="")
            log_milestone("Documents indexed")
            
        return existing_files

    def load_existing_index(self):
        log_secure_action("load", file_name="")
        log_milestone("Loading FAISS index")
        
        # When loading from disk, temporarily initialize a store with a generic dimension
        # because the internal .load() method will overwrite self.index anyway.
        self.store = VectorStore(dimension=768)
        self.store.load(FAISS_PATH, METADATA_PATH)
        
        if hasattr(self.store, 'documents') and self.store.documents:
            self.total_chunks = len(self.store.documents)
            self.indexed_files_list = {"Pre-existing Documents"}

    @staticmethod
    def has_existing_index():
        return os.path.exists(f"{FAISS_PATH}.index")
'''

#Aug 6 test
import os
from app.vector_store import VectorStore
from app.embeddings import generate_embedding
from app.rag_preparation import prepare_document
from app.logger import log_secure_action, log_milestone

# Path mappings
FAISS_PATH = "storage/faiss/faiss_store"
METADATA_PATH = "storage/metadata/faiss_store"

class Retriever:
    def __init__(self):
        # Dynamically scales to match your structural layout sizes on first run
        self.store = None
        self.total_chunks = 0
        self.indexed_files_list = set()

    def add_document(self, text):
        embedding = generate_embedding(text)
        if self.store is None:
            self.store = VectorStore(dimension=len(embedding))
        
        # Fallback dictionary matching new enterprise structural layouts
        fallback_item = {
            "text": text,
            "filename": "Direct_Text_Injection.txt",
            "chunk_number": 1,
            "page": 1
        }
        self.store.add(embedding, fallback_item)

    def search(self, question):
        log_secure_action("search", file_name="", count=3)
        embedding = generate_embedding(str(question))
        if self.store is None:
            return []
        
        # Task 2: Returns the complete matching object collection from our index data
        return self.store.search(embedding)

    def index_document(self, file_path):
        file_path = str(file_path)
        filename = os.path.basename(file_path)
        
        # Invokes your standard preparation step safely
        chunks = prepare_document(file_path)
        
        for idx, item in enumerate(chunks):
            emb = item.get("embedding") if "embedding" in item else generate_embedding(item["text"])
            
            if self.store is None:
                self.store = VectorStore(dimension=len(emb))
                
            # Task 1: Complete Metadata Dictionary Construction (Default page to 1 for flat files)
            structured_payload = {
                "text": item["text"],
                "filename": filename,
                "chunk_number": idx + 1,
                "page": 1
            }
            
            # Pass the complete dictionary directly into your Vector Store engine
            self.store.add(emb, structured_payload)
            
        self.total_chunks += len(chunks)
        self.indexed_files_list.add(filename)
        log_secure_action("index_file", file_name=file_path, count=len(chunks))

    def build_index(self, upload_dir):
        self.total_chunks = 0
        self.indexed_files_list.clear()
        
        if not os.path.exists(upload_dir):
            return []
            
        existing_files = [f for f in os.listdir(upload_dir) if f.endswith(('.txt', '.csv'))]
        for existing_file in existing_files:
            file_path = os.path.join(upload_dir, existing_file)
            try:
                self.index_document(file_path)
            except Exception as e:
                print(f"Error pre-indexing {existing_file}: {e}")
                
        if self.store is not None and len(self.store.documents) > 0:
            os.makedirs(os.path.dirname(FAISS_PATH), exist_ok=True)
            os.makedirs(os.path.dirname(METADATA_PATH), exist_ok=True)
            self.store.save(FAISS_PATH, METADATA_PATH)
            log_secure_action("create", file_name="")
            log_milestone("Documents indexed")
            
        return existing_files

    def load_existing_index(self):
        log_secure_action("load", file_name="")
        log_milestone("Loading FAISS index")
        
        # Temporarily scale base vector dimension
        self.store = VectorStore(dimension=1536)
        self.store.load(FAISS_PATH, METADATA_PATH)
        
        if hasattr(self.store, 'documents') and self.store.documents:
            self.total_chunks = len(self.store.documents)
            
            # Reconstruct unique index collections securely from stored dictionary frames
            unique_files = set()
            for doc in self.store.documents:
                if isinstance(doc, dict) and "filename" in doc:
                    unique_files.add(doc["filename"])
            
            if unique_files:
                self.indexed_files_list = unique_files
            else:
                self.indexed_files_list = {"Loaded Corporate Assets"}

    @staticmethod
    def has_existing_index():
        return os.path.exists(f"{FAISS_PATH}.index")
