from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

NOTES_DIR = PROJECT_ROOT / "notes"
CHROMA_DIR = PROJECT_ROOT / ".chroma"
COLLECTION_NAME = "learn_ai_notes"

EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
