import requests
from src.config import OLLAMA_MODEL, OLLAMA_BASE_URL


SYSTEM_PROMPT = """You are an academic research assistant.

You may ONLY use the provided context.
Do NOT use prior knowledge.
Do NOT guess.

Write a clear academic answer based strictly on the context.
Do NOT include citations.
Do NOT mention page numbers or paper IDs.

If unsupported, output exactly:
Not supported by the provided papers.
"""


class OllamaClient:
    def __init__(self):
        self.model = OLLAMA_MODEL
        self.base_url = OLLAMA_BASE_URL.rstrip("/")

    def generate(self, query: str, context_chunks):
        context_text = ""

        for chunk in context_chunks:
            context_text += (
                f"[{chunk['paper_id']}, p.{chunk['page']}]\n"
                f"{chunk['text']}\n\n"
            )

        prompt = f"""
Context:
{context_text}

Question:
{query}

Answer:
"""

        payload = {
            "model": self.model,
            "prompt": SYSTEM_PROMPT + "\n\n" + prompt,
            "stream": False,
            "options": {"temperature": 0.1}
        }

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=180
        )

        if response.status_code != 200:
            raise Exception(f"Ollama generation failed: {response.text}")

        return response.json().get("response", "").strip()

