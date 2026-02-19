import httpx
import json
from typing import AsyncGenerator, List, Dict, Any, Optional
from app.core.config import settings
from app.services.llm.base import LLMProvider

class OllamaProvider(LLMProvider):
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL

    async def generate_stream(self, messages: List[Dict[str, Any]], model: str = None, temperature: float = 0.7, tools: List[Any] = None) -> AsyncGenerator[str, None]:
        # Ollama tools support is experimental/different. For now, we will focus on pure chat.
        # If tools are strictly needed, we might need a specific prompt engineering approach or newer Ollama features.
        # The prompt instructed "The chat must work", tools are "Extra".
        # We will implement basic chat stream first.
        
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": model or self.model,
            "messages": messages,
            "options": {
                "temperature": temperature
            },
            "stream": True
        }

        try:
            async with httpx.AsyncClient() as client:
                async with client.stream("POST", url, json=payload, timeout=None) as response:
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                chunk = json.loads(line)
                                if "message" in chunk and "content" in chunk["message"]:
                                    yield chunk["message"]["content"]
                                if chunk.get("done", False):
                                    break
                            except json.JSONDecodeError:
                                continue
        except Exception as e:
            print(f"Error in Ollama stream: {e}")
            yield f"Error connecting to Ollama: {str(e)}"

    async def generate(self, messages: List[Dict[str, Any]], model: str = None, temperature: float = 0.7, tools: List[Any] = None) -> str:
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": model or self.model,
            "messages": messages,
            "options": {
                "temperature": temperature
            },
            "stream": False
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=60.0)
                response.raise_for_status()
                result = response.json()
                return result["message"]["content"]
        except Exception as e:
            print(f"Error in Ollama generate: {e}")
            return f"Error connecting to Ollama: {str(e)}"

class LLMFactory:
    @staticmethod
    def get_provider() -> LLMProvider:
        return OllamaProvider()
