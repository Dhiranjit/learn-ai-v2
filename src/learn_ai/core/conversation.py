from learn_ai.db.store import ConversationStore
from learn_ai.llm.client import LLMClient
from learn_ai.observability.tracing import Trace


class Conversation:
    def __init__(
            self,
            client: LLMClient,
            store: ConversationStore,
            notebook_id: int,
            system_prompt: str | None = None,
            ):
        self.client = client
        self.store = store
        self.notebook_id = notebook_id
        self.traces: list[Trace] = []
        self.messages = store.load_messages(notebook_id)
        if not self.messages and system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})
            store.append_message(notebook_id, "system", system_prompt)

    def send(self, message: str) -> str:
        trace = Trace()
        trace.stage(name="conversation_history", value=self.messages.copy())

        self.messages.append({"role": "user", "content": message})
        self.store.append_message(self.notebook_id, "user", message)

        trace.stage(name="llm_input", value=self.messages.copy())

        reply = self.client.chat(self.messages)

        trace.stage(name="llm_output", value=reply)

        self.traces.append(trace)
        self.messages.append({"role": "assistant", "content": reply})
        self.store.append_message(self.notebook_id, "assistant", reply)
        return reply
