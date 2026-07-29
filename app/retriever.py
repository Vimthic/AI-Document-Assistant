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
'''
#for FAISS index store
import os
from app.vector_store import VectorStore
from app.embeddings import generate_embedding
from app.rag_preparation import prepare_document
# Import your security-focused logging helpers
from app.logger import log_secure_action, log_milestone

# Define separate storage paths based on your new directory architecture
FAISS_PATH = "storage/faiss/faiss_store"
METADATA_PATH = "storage/metadata/faiss_store"

class Retriever:
    def __init__(self):
        # 1. Generate a dummy embedding to find the actual dimension size dynamically
        sample_embedding = generate_embedding("test")
        actual_dimension = len(sample_embedding)
 
        # 2. Pass the correct dimension to your VectorStore (Named 'store' to preserve your code)
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
        # Safe Logging: Signals a search is starting without logging the actual user question
        log_secure_action("search", file_name="", count=3)
        
        embedding = generate_embedding(
            question
        )
        return self.store.search(
            embedding
        )

    def index_document(self, file_path):
        chunks = prepare_document(file_path)
        for item in chunks:
            # Check if preparation already parsed embeddings, otherwise build dynamically
            emb = item.get("embedding") if "embedding" in item else generate_embedding(item["text"])
            self.store.add(
                emb,
                item["text"]
            )
        # Safe Logging: Logs file completion with a safe chunk count metric
        log_secure_action("index_file", file_name=file_path, count=len(chunks))

    def build_index(self, upload_dir):
        """Scans the physical uploads folder to parse and index flat raw files."""
        existing_files = [f for f in os.listdir(upload_dir) if f.endswith(('.txt', '.csv'))]
        for existing_file in existing_files:
            file_path = os.path.join(upload_dir, existing_file)
            try:
                self.index_document(file_path)
            except Exception as e:
                print(f"Error pre-indexing {existing_file}: {e}")
                
        # Persist index arrays and metadata tables cleanly if content loaded
        if len(self.store.documents) > 0:
            # Create directories dynamically if they do not exist
            os.makedirs(os.path.dirname(FAISS_PATH), exist_ok=True)
            os.makedirs(os.path.dirname(METADATA_PATH), exist_ok=True)
            
            # Save using our new split folder layout routes
            self.store.save(FAISS_PATH, METADATA_PATH)
            
            # Safe Logging: Confirms a secure new index creation event
            log_secure_action("create", file_name="")
            log_milestone("Documents indexed")
            
        return existing_files

    def load_existing_index(self):
        """Restores memory footprints from existing storage arrays."""
        # Safe Logging: Marks index restoration activity clearly
        log_secure_action("load", file_name="")
        logger_msg = "Loading FAISS index" # Match historical logging strings safely
        log_milestone(logger_msg)
        
        self.store.load(FAISS_PATH, METADATA_PATH)

    @staticmethod
    def has_existing_index():
        """Checks if persistent index file twins sit inside their respective storage directories."""
        return os.path.exists(f"{FAISS_PATH}.index") and os.path.exists(f"{METADATA_PATH}.json")
