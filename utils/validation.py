from fastapi import HTTPException
from typing import Any
from models.provider_response import ErrorResponse

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
                detail=[{"msg": f"Error from {response.provider}: {response.error}"}]
            )