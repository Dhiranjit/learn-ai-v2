from dataclasses import is_dataclass, asdict

import streamlit as st


def _to_jsonable(value):
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, dict):
        return {k: _to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(v) for v in value]
    return str(value)


def _render(value) -> None:
    if value is None:
        st.caption("_(empty)_")
    elif isinstance(value, (dict, list)):
        st.json(_to_jsonable(value))
    else:
        st.code(str(value), language="markdown")


def main() -> None:
    st.set_page_config(page_title="Traces — Learn AI", layout="wide")
    st.title("Conversation traces")
    st.caption("In-memory traces for this session. Refreshing the page clears them.")

    conversations = st.session_state.get("conversations", {})
    if not conversations:
        st.info("No active conversations yet. Send a message in the chat first.")
        return

    options = {}
    for nb_id, conv in conversations.items():
        count = len(conv.traces)
        options[f"Notebook #{nb_id} · {count} trace(s)"] = nb_id

    label = st.selectbox("Conversation", list(options.keys()))
    conv = conversations[options[label]]

    if not conv.traces:
        st.info("This conversation has no traces yet.")
        return

    trace_labels = [
        f"#{i + 1} · {len(t.stages)} stage(s)"
        for i, t in enumerate(conv.traces)
    ]
    idx = st.selectbox(
        "Trace",
        range(len(conv.traces)),
        format_func=lambda i: trace_labels[i],
        index=len(conv.traces) - 1,
    )
    trace = conv.traces[idx]

    st.subheader(f"Trace #{idx + 1}")

    for i, stage in enumerate(trace.stages, start=1):
        with st.expander(f"[{i}] {stage.name}", expanded=False):
            _render(stage.value)


main()
