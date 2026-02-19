from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Dict, Any

class LLMProvider(ABC):
    @abstractmethod
    async def generate_stream(self, messages: List[Dict[str, str]], model: str, temperature: float = 0.7, tools: List[Any] = None) -> AsyncGenerator[str, None]:
        """
        Generate a streaming response from the LLM.
        """
        pass

    @abstractmethod
    async def generate(self, messages: List[Dict[str, str]], model: str, temperature: float = 0.7, tools: List[Any] = None) -> str:
        """
        Generate a complete response from the LLM.
        """
        pass
