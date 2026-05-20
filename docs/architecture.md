# Architecture

Current state of the project.

## Component hierarchy

```
┌──────────────────────────────────────────────┐
│  frontend/app.py            (Streamlit UI)   │
│    - sidebar: notebook list, new chat        │
│    - main:    chat bubbles + input           │
│  frontend/pages/traces.py   (trace viewer)   │
└──────────────────┬───────────────────────────┘
                   │ uses
                   ▼
┌──────────────────────────────────────────────┐
│  core/conversation.py       (Conversation)   │
│    - holds message list for one notebook     │
│    - write-through: memory + DB per turn     │
└──┬──────────────────┬──────────────────┬─────┘
   │ uses             │ uses             │ uses
   ▼                  ▼                  ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────────┐
│ llm/client   │ │ db/store     │ │ observability/   │
│ (LLMClient)  │ │ (Conv.Store) │ │   tracing.py     │
│ - chat(msgs) │ │ - notebooks  │ │ - span context   │
│ - strip<thk> │ │ - messages   │ │ - persists spans │
└──────┬───────┘ └──────┬───────┘ └────────┬─────────┘
       │ uses           │ uses             │ writes
       ▼                ▼                  ▼
┌──────────────┐ ┌──────────────┐    SQLite (traces)
│ llm/providers│ │ db/schema    │
│ - api keys   │ │ - tables     │
│ - base URLs  │ │              │
└──────┬───────┘ └──────┬───────┘
       │                │
       ▼                ▼
 OpenAI-compatible  SQLite
 API (Groq/NVIDIA)  (learn_ai.db)
```

### RAG pipeline

A standalone linear pipeline in `src/learn_ai/rag/`. End-to-end functional; not yet wired into `Conversation`.

```
notes/*.md  ──►  loader.py   ──►  Document(source, text)
                                       │
                                       ▼
                                  chunker.py   ──►  Chunk(source, chunk_id, text)
                                       │
                                       ▼
                                  index.py     ──►  Chroma collection (.chroma/)
                                       │                (bge-base-en-v1.5, cosine)
                                       ▼
                                  retriever.py ──►  top-k chunks for a query
```

- `config.py` — paths, collection name, embedding model, chunk size/overlap
- Embedding is delegated to Chroma's `SentenceTransformerEmbeddingFunction` so the same model runs at index and query time
- Chunk ids are deterministic (`source::chunk_id`) so re-indexing edited notes upserts rather than duplicates
- `retriever.py` returns `Retrieved(source, chunk_id, text, score)` with `score = 1 - cosine_distance`; empty queries short-circuit to `[]`

## Data flow — one chat turn

1. User types into Streamlit chat input.
2. `app.py` calls `Conversation.send(prompt)`.
3. `Conversation` appends the user message to `self.messages` and persists it via `ConversationStore.append_message`.
4. `Conversation` calls `LLMClient.chat(self.messages)`.
5. `LLMClient` sends the full message history to the provider, receives a reply, strips `<think>` blocks, returns the clean reply.
6. `Conversation` appends the assistant reply to `self.messages` and persists it.
7. `app.py` renders the reply.

## Design principles in play

- **Frontend is thin** — `app.py` knows nothing about SQL or LLM APIs. It only calls into `core/` and `db/`.
- **`LLMClient` is transport** — takes a message list, returns a string. Provider-specific quirks (e.g. think tags) are absorbed here so callers stay model-agnostic.
- **DB is the source of truth** — `Conversation` keeps an in-memory cache for the active session but writes through to SQLite on every turn. Reloading reconstructs state from the DB.
- **Notebook-scoped** — every message belongs to a `notebook_id`; conversations don't bleed across notebooks.

## Not yet built

- `api/` — HTTP layer (for when we outgrow Streamlit).
- `memory/` — persistent cross-notebook memory.
- RAG ↔ `Conversation` integration — retrieval results are not yet injected into the LLM call.

## Recently built

- `observability/tracing.py` — structured span tracing, persisted to SQLite. Viewed via `frontend/pages/traces.py`.
- `rag/` — full pipeline (`loader → chunker → index → retriever`) using Chroma + `bge-base-en-v1.5`. Standalone; awaiting integration with `Conversation`.
