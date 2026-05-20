from dataclasses import dataclass

from learn_ai.rag.config import CHUNK_SIZE, CHUNK_OVERLAP
from learn_ai.rag.loader import Document


@dataclass
class Chunk:
    source: str
    chunk_id: int
    text: str

    @property
    def id(self) -> str:
        return f"{self.source}::{self.chunk_id}"


def split_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    if size <= 0 or overlap >= size:
        raise ValueError("Invalied chunk size/overlap")
    start = 0
    chunks = []
    while (start < len(text)):
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


def chunk_documents(docs: list[Document]) -> list[Chunk]:
    out = []
    for doc in docs:
        for i, split in enumerate(split_text(doc.text)):
            out.append(Chunk(source=doc.source, chunk_id=i, text=split))
    return out

