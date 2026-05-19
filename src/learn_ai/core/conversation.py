import time

from learn_ai.db.store import ConversationStore
from learn_ai.llm.client import LLMClient
from learn_ai.observability.tracing import Tracer


class Conversation:
    def __init__(
            self,
            client: LLMClient,
            store: ConversationStore,
            notebook_id: int,
            system_prompt: str | None = None,
            tracer: Tracer | None = None,
            ):
        self.client = client
        self.store = store
        self.notebook_id = notebook_id
        self.tracer = tracer
        self.messages = store.load_messages(notebook_id)
        if not self.messages and system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})
            store.append_message(notebook_id, "system", system_prompt)

    def send(self, message: str) -> str:
        self.messages.append({"role": "user", "content": message})
        self.store.append_message(self.notebook_id, "user", message)

        trace = self.tracer.start_trace(self.notebook_id, message) if self.tracer else None

        if trace:
            trace.stage(
                "load_history",
                input={"notebook_id": self.notebook_id},
                output=self.messages,
                meta={"message_count": len(self.messages)},
            )

        t0 = time.perf_counter()
        reply = self.client.chat(self.messages)
        llm_ms = int((time.perf_counter() - t0) * 1000)

        if trace:
            trace.stage(
                "llm_call",
                input={"messages": self.messages, "model": self.client.model},
                output=reply,
                meta={"model": self.client.model},
                duration_ms=llm_ms,
            )
            trace.end()

        self.messages.append({"role": "assistant", "content": reply})
        self.store.append_message(self.notebook_id, "assistant", reply)
        return reply
