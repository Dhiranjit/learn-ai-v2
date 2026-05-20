from pathlib import Path
from dataclasses import dataclass

from learn_ai.rag.config import NOTES_DIR


@dataclass
class Document:
    source: str # relative path, used as an id later
    text: str


def load_notes(notes_dir: Path = NOTES_DIR) -> list[Document]:
    docs = []
    for path in sorted(notes_dir.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if text.strip():
            docs.append(Document(source=str(path.relative_to(notes_dir)), text=text))
    return docs


if __name__ == "__main__":
    docs = load_notes()
    print(f"Loaded {len(docs)} notes")
    for d in docs[:3]:
        print(f"- {d.source} ({len(d.text)} chars)")
