import json
from learn_ai.db.store import ConversationStore
from learn_ai.llm.client import LLMClient
from learn_ai.observability.tracing import Trace
from learn_ai.llm.tools import TOOLS, TOOLS_REGISTRY


MAX_ITER = 4

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

        for _ in range(MAX_ITER):
            trace.stage(name="llm_input", value=self.messages.copy())
            reply = self.client.chat(self.messages, tools=TOOLS)
            trace.stage(name="llm_output", value=reply.model_dump())

            assistant_msg = reply.model_dump(exclude_none=True)
            assistant_msg.pop("reasoning", None)
            self.messages.append(assistant_msg)
            self.store.append_message(self.notebook_id, "assistant", json.dumps(assistant_msg))

            if not reply.tool_calls:
                self.traces.append(trace)
                return reply.content
            
            for call in reply.tool_calls:
                fn = TOOLS_REGISTRY[call.function.name]
                args = json.loads(call.function.arguments)
                result = fn(**args)
                tool_msg = {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": str(result)
                }

                self.messages.append(tool_msg)
                self.store.append_message(self.notebook_id, "tool", json.dumps(tool_msg))
            
        self.traces.append(trace)
        return "[max iterations reached]"