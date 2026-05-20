import chromadb
from chromadb.utils import embedding_functions

from learn_ai.rag.config import CHROMA_DIR, COLLECTION_NAME,EMBEDDING_MODEL
from learn_ai.rag.chunker import Chunk


def get_collection():
    """
    Open (or create) the persisitant Chroma collection
    for our notes.
    """
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embed_fn,
        metadata={"hnsw:space" : "cosine"}
    )

def index_chunks(chunks: list[Chunk]) -> None:
    """Embed and upsert chunks into the collection"""
    if not chunks:
        return
    collection = get_collection()
    collection.upsert(
        ids=[c.id for c in chunks],
        documents=[c.text for c in chunks],
        metadatas=[{"source": c.source, "chunk_id" : c.chunk_id} for c in chunks]
    )