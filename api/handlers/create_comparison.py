import asyncio
from datetime import datetime
from fastapi import HTTPException
from models.api_request import ComparisonRequest
from models.api_response import ComparisonResponse, TimedCallResponse
from services import OpenAIService, AnthropicService, XAIService
from services.base_service import BaseAIService
from utils.response_processor import process_response
from utils.validation import validate_request, validate_error_response, validate_rate_limit

async def timed_call(service: BaseAIService, prompt: str):
    start_time = datetime.now()
    result = await service.get_completion(prompt)
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()   
    return TimedCallResponse(
        service_name=service.get_provider_name(),
        result=result,
        start_time=start_time,
        end_time=end_time,
        duration=duration
    )

async def create_comparison(request: ComparisonRequest) -> ComparisonResponse :
    """
    Send the same prompt to all three AI models simultaneously and return their responses.
    
    Args:
        request: JSON payload containing prompt
    """

    validate_request(request, "prompt")
    validate_rate_limit()
    
    actual_prompt = request.prompt
    services = [OpenAIService(), AnthropicService(), XAIService()]
    
    # Run all API calls concurrently with error handling and timeout
    tasks = [asyncio.create_task(timed_call(service, actual_prompt)) for service in services]
    try:
        responses = await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), timeout=5.0)
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=408,
            detail=[{"msg": "API timeout exception"}]
        )
    
    # Validate responses and process
    validate_error_response(responses)
    processed_responses = [process_response(response.result, response.duration) for response in responses]
    
    return ComparisonResponse(
        user_prompt = actual_prompt,
        responses = processed_responses
    )