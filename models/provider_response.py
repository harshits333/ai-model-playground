from typing import Optional
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    model: str
    provider: str
    error: str

class AIResponse(BaseModel):
    content: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    model: str
    cost: float
    provider: str
    error: Optional[str] = None