from abc import ABC, abstractmethod
from typing import Dict, Any, Type
from pydantic import BaseModel

class Tool(ABC):
    name: str
    description: str
    args_schema: Type[BaseModel]

    @abstractmethod
    def run(self, **kwargs) -> Any:
        pass
