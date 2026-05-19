from datetime import datetime

import streamlit as st

from learn_ai.core.conversation import Conversation
from learn_ai.db.store import ConversationStore
from learn_ai.llm.client import LLMClient
from learn_ai.observability.tracing import Tracer


PROVIDER = "groq"
MODEL = "qwen/qwen3-32b"
SYSTEM_PROMPT = "You are a helpful AI tutor. Explain concepts clearly and ask guiding questions."


@st.cache_resource
def get_store() -> ConversationStore:
    return ConversationStore("learn_ai.db")


@st.cache_resource
def get_client() -> LLMClient:
    return LLMClient(provider=PROVIDER, model=MODEL)


@st.cache_resource
def get_tracer() -> Tracer:
    return Tracer("learn_ai.db")


def get_conversation(notebook_id: int) -> Conversation:
    cache = st.session_state.setdefault("conversations", {})
    if notebook_id not in cache:
        cache[notebook_id] = Conversation(
            client=get_client(),
            store=get_store(),
            notebook_id=notebook_id,
            system_prompt=SYSTEM_PROMPT,
            tracer=get_tracer(),
        )
    return cache[notebook_id]


def render_sidebar() -> None:
    store = get_store()
    st.sidebar.title("Learn AI")

    if st.sidebar.button("+ New chat", use_container_width=True):
        title = f"New chat {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        st.session_state["active_notebook"] = store.create_notebook(title)
        st.rerun()

    st.sidebar.markdown("### Notebooks")
    notebooks = store.list_notebooks()
    if not notebooks:
        st.sidebar.caption("No notebooks yet. Start a new chat.")
        return

    active = st.session_state.get("active_notebook")
    for nb in notebooks:
        label = nb["title"]
        is_active = nb["id"] == active
        if st.sidebar.button(
            ("• " if is_active else "  ") + label,
            key=f"nb-{nb['id']}",
            use_container_width=True,
        ):
            st.session_state["active_notebook"] = nb["id"]
            st.rerun()


def render_chat(notebook_id: int) -> None:
    conv = get_conversation(notebook_id)

    for msg in conv.messages:
        if msg["role"] == "system":
            continue
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Write a message...")
    if not prompt:
        return

    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = conv.send(prompt)
        st.markdown(reply)


def main() -> None:
    st.set_page_config(page_title="Learn AI", layout="wide")
    render_sidebar()

    notebook_id = st.session_state.get("active_notebook")
    if notebook_id is None:
        st.title("Learn AI")
        st.caption("Select a notebook from the sidebar, or start a new chat.")
        return

    render_chat(notebook_id)


if __name__ == "__main__":
    main()
