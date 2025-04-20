import yaml
from fastapi import HTTPException
from typing import Any
from models.provider_response import ErrorResponse
from utils.rate_limiter import RateLimiter
from pathlib import Path

def validate_request(request: Any, required_field: str) -> None:
    """
    Validate that a request contains the required field.
    
    Args:
        request: The request object to validate
        required_field: The field that must be present in the request
    
    Raises:
        HTTPException: 422 if required field is missing
    """
    if not request or not hasattr(request, required_field) or not getattr(request, required_field):
        raise HTTPException(
            status_code=422,
            detail=[{"msg": f"{required_field} field required in request body"}]
        )

def validate_error_response(responses: Any) -> None:
    """
    Validate that a response is not an ErrorResponse.
    
    Args:
        response: The response object to validate
    
    Raises:
        HTTPException: 500 if response is an ErrorResponse
    """
    for response in responses:
        if isinstance(response.result, ErrorResponse):
            raise HTTPException(
                status_code=500,
                detail=[{"msg": f"Error : {response.error}"}]
            )
            
def validate_rate_limit() -> None:
    """
    Validate that the request doesn't exceed global rate limits.
    
    Raises:
        HTTPException: 429 if rate limit is exceeded
    """
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path) as f:
        conf = yaml.safe_load(f)
    config = conf["api"]
    rate_limiter = RateLimiter(
                entity="api",
                rate_limit=config["rate_limit"],
                rate_limit_window=config["rate_limit_window"]
            )
    if not rate_limiter.check_limit():
        raise HTTPException(
            status_code=429,
            detail=[{"msg": "Rate limit exceeded"}]
        )