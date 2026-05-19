import json

import streamlit as st

from learn_ai.db.store import ConversationStore
from learn_ai.observability.tracing import Tracer


@st.cache_resource
def get_tracer() -> Tracer:
    return Tracer("learn_ai.db")


@st.cache_resource
def get_store() -> ConversationStore:
    return ConversationStore("learn_ai.db")


def _pretty(value: str | None):
    if value is None:
        return None
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return value


def _render(value) -> None:
    if value is None:
        st.caption("_(empty)_")
    elif isinstance(value, (dict, list)):
        st.json(value)
    else:
        st.code(str(value), language="markdown")


def main() -> None:
    st.set_page_config(page_title="Traces — Learn AI", layout="wide")
    st.title("Conversation traces")
    st.caption("Inspect what was sent to the LLM at each layer of context building.")

    tracer = get_tracer()
    store = get_store()

    notebooks = store.list_notebooks()
    options = {"All notebooks": None} | {nb["title"]: nb["id"] for nb in notebooks}
    choice = st.selectbox("Notebook", list(options.keys()))
    notebook_id = options[choice]

    traces = tracer.list_traces(notebook_id=notebook_id, limit=100)
    if not traces:
        st.info("No traces yet. Send a message in the chat to generate one.")
        return

    labels = [
        f"#{t['id']} · {t['started_at']} · {(t['user_message'] or '')[:60]}"
        f" · {t['duration_ms'] or '?'} ms"
        for t in traces
    ]
    idx = st.selectbox("Trace", range(len(traces)), format_func=lambda i: labels[i])
    trace = traces[idx]

    st.subheader(f"Trace #{trace['id']}")
    st.write(
        {
            "notebook_id": trace["notebook_id"],
            "user_message": trace["user_message"],
            "started_at": trace["started_at"],
            "duration_ms": trace["duration_ms"],
        }
    )

    stages = tracer.get_stages(trace["id"])
    for stage in stages:
        header = f"[{stage['ord']}] {stage['name']}"
        if stage["duration_ms"] is not None:
            header += f" · {stage['duration_ms']} ms"
        with st.expander(header, expanded=False):
            col_in, col_out = st.columns(2)
            with col_in:
                st.markdown("**Input**")
                _render(_pretty(stage["input_json"]))
            with col_out:
                st.markdown("**Output**")
                _render(_pretty(stage["output_json"]))
            meta = _pretty(stage["meta_json"])
            if meta:
                st.markdown("**Meta**")
                _render(meta)


main()
