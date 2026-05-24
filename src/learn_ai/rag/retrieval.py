from dataclasses import dataclass
from learn_ai.rag.index import get_collection


@dataclass
class Retrieved:
    source: str
    chunk_id: int
    text: str
    score: float

    @property
    def id(self) -> str:
        return f"{self.source}::{self.chunk_id}"
    

def retriever(query: str, top_k: int = 5) -> list[Retrieved]:
    """Return the top-k most semantically similar chunks for `query`."""
    if not query.strip():
        return []
    
    collection = get_collection()
    res = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    docs = res["documents"][0]
    metas = res["metadatas"][0]
    distances = res["distances"][0]

    return [
        Retrieved(
            source=meta["source"],
            chunk_id=meta["chunk_id"],
            text=doc,
            score=1.0 - dist
        )
        for doc, meta, dist in zip(docs, metas, distances)
    ]