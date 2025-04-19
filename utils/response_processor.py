from models.provider_response import AIResponse
from models.api_response import ModelResponse

def process_response(resp: AIResponse, latency: int) -> ModelResponse:
    """
    Process a single AI service response into a standardized format.
    
    Args:
        resp: The response from AI service or an exception
        response_time_ms: Total response time in milliseconds
    
    Returns:
        ModelResponse: Standardized response format
    """
    return ModelResponse(
        provider=resp.provider,
        model=resp.model,
        content=resp.content,
        prompt_tokens=resp.prompt_tokens,
        completion_tokens=resp.completion_tokens,
        total_tokens=resp.total_tokens,
        cost=resp.cost,
        latency=latency
    )