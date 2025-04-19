from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session
from models.api_response import ModelResponse
from repositories.comparison import Comparison
from repositories.model_response import ModelResponseDB

def save_comparison(db: Session, prompt: str, processed_responses: List[ModelResponse]) -> Comparison:
    """
    Save comparison and responses to database
    """
    try:
        comparison = Comparison(user_prompt=prompt)
        db.add(comparison)
        db.commit()
        db.refresh(comparison)
        
        db_responses = []
        for resp in processed_responses:
            db_responses.append(ModelResponseDB(
                model=resp.model,
                content=resp.content,
                prompt_tokens=resp.prompt_tokens,
                completion_tokens=resp.completion_tokens,
                total_tokens=resp.total_tokens,
                cost=resp.cost,
                comparison_id=comparison.id,
                provider=resp.provider,
                latency=resp.latency
            ))
        
        db.add_all(db_responses)
        db.commit()

        return comparison
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))