from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    role: str
    content: str
    
class ChatRequest(BaseModel):
    messages: List[Message]
    model: str = "gpt-4o-mini"
    conversation_id: Optional[int] = None
    stream: bool = True

class ChatResponse(BaseModel):
    content: str
