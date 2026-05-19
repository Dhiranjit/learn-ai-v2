# Architecture

Current state of the project.

## Component hierarchy

```
┌──────────────────────────────────────────────┐
│  frontend/app.py            (Streamlit UI)   │
│    - sidebar: notebook list, new chat        │
│    - main:    chat bubbles + input           │
└──────────────────┬───────────────────────────┘
                   │ uses
                   ▼
┌──────────────────────────────────────────────┐
│  core/conversation.py       (Conversation)   │
│    - holds message list for one notebook     │
│    - write-through: memory + DB per turn     │
└──────┬───────────────────────────┬───────────┘
       │ uses                      │ uses
       ▼                           ▼
┌────────────────────┐   ┌────────────────────────┐
│  llm/client.py     │   │  db/store.py           │
│  (LLMClient)       │   │  (ConversationStore)   │
│  - chat(messages)  │   │  - create_notebook     │
│  - strips <think>  │   │  - list_notebooks      │
│                    │   │  - append_message      │
│                    │   │  - load_messages       │
└─────────┬──────────┘   └───────────┬────────────┘
          │ uses                     │ uses
          ▼                          ▼
┌────────────────────┐   ┌────────────────────────┐
│  llm/providers.py  │   │  db/schema.py          │
│  - api keys        │   │  - notebooks table     │
│  - base URLs       │   │  - messages table      │
└─────────┬──────────┘   └───────────┬────────────┘
          │                          │
          ▼                          ▼
   OpenAI-compatible API      SQLite (learn_ai.db)
   (Groq / NVIDIA / ...)
```

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
- `rag/` — retrieval-augmented generation over uploaded docs.
- `memory/` — persistent cross-notebook memory.
- `observability/` — structured tracing / logging.
