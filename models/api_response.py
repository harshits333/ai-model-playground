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
    error: Optional[str] = None 

class ComparisonResponse(BaseModel):
    id: int
    user_prompt: str
    created_at: datetime
    responses: List[ModelResponse]

    @classmethod
    def from_db(cls, comparison, processed_responses):
        return cls(
            id=comparison.id,
            user_prompt=comparison.user_prompt,
            created_at=comparison.created_at,
            responses=processed_responses
        )