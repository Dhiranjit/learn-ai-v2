"""Defines the tools that LLM can call (uses OpenAI format)"""
from learn_ai.rag.retrieval import retriever


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "retrieve_context",
            "description": "Retrieve relevant chunks from the vector database for answering user queries.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string"
                    },
                    "top_k": {
                        "type": "integer",
                        "default": 5
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        }
    }
]


def _retrive_context(query: str, top_k: int = 5) -> str:
    results = retriever(query, top_k)

    if not results:
        return "No relevant context found."
    return "\n\n".join(
        f"[{r.source} # {r.chunk_id} score={r.score:.2f}]\n{r.text}"
        for r in results
        )

TOOLS_REGISTRY = {
    "retrieve_context": _retrive_context,
}