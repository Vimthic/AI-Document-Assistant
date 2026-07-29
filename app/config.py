from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FOLDER = PROJECT_ROOT / "data"

STORAGE_FOLDER = PROJECT_ROOT / "storage"

FAISS_FOLDER = STORAGE_FOLDER / "faiss"

UPLOAD_FOLDER = STORAGE_FOLDER / "uploads"

METADATA_FOLDER = STORAGE_FOLDER / "metadata"