from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel

class TimedCallResponse(BaseModel):
    service_name: str
    result: Any
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    duration: Optional[float]
    error: Optional[str] = None 

class ModelResponse(BaseModel):
    provider: str
    model: str
    content: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: float
    latency: float

class ComparisonResponse(BaseModel):
    user_prompt: str
    responses: List[ModelResponse]

class ComparisonDBResponse(BaseModel):
    id: int
    created_at: datetime
    user_prompt: str
    responses: List[ModelResponse]