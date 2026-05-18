from learn_ai.llm.client import LLMClient
from learn_ai.db.store import ConversationStore

class Conversation:
    def __init__(
            self,
            client: LLMClient, 
            store: ConversationStore,
            notebook_id: int,
            system_prompt:str | None = None
            ):
        self.client = client
        self.store = store
        self.notebook_id = notebook_id
        self.messages = store.load_messages(notebook_id)
        if not self.messages and system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})
            store.append_message(notebook_id, "system", system_prompt)
    
    def send(self, message: str) -> str:
        self.messages.append({"role": "user", "content": message})
        self.store.append_message(self.notebook_id, "user", message)
        reply = self.client.chat(self.messages)
        self.messages.append({"role": "assistant", "content": reply})
        self.store.append_message(self.notebook_id, "assistant", reply)
        return reply
