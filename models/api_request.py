from pydantic import BaseModel

class ComparisonRequest(BaseModel):
    prompt: str