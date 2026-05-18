from openai import OpenAI
from learn_ai.llm.providers import PROVIDERS


class LLMClient:
    def __init__(self, provider: str, model: str):
    
        config = PROVIDERS.get(provider)
        if not config:
            raise ValueError(f"Unknown provider: {provider}")
        
        self.model = model
        self.client = OpenAI(
            api_key=config["api_key"],
            base_url=config["base_url"]
        )
    
    def chat(self, messages: list[dict]):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content
