from fastapi import HTTPException
from repositories.comparison_repository import save_comparison
from models.api_response import ModelResponse
from database import SessionLocal
from typing import List

async def save_comparison_handler(actual_prompt: str, processed_responses: List[ModelResponse]) -> int:
    """
    Save the comparison results to the database.

    Args:
        actual_prompt: The prompt sent to the AI models.
        processed_responses: The processed responses from the AI models.

    Returns:
        A ComparisonResponse object containing the saved comparison data.
    """
    db = SessionLocal()
    try:
        comparison = save_comparison(db, actual_prompt, processed_responses)
        return comparison.id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()