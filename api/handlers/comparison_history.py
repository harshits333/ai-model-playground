from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import joinedload
from models.api_response import ComparisonResponse
from repositories.comparison import Comparison
from database import SessionLocal

def get_comparison_history() -> List[ComparisonResponse]:
    """
    Retrieve all historical comparisons with their model responses.
    """
    db = SessionLocal()
    try:
        comparisons = db.query(Comparison).options(joinedload(Comparison.responses)).all()
        return comparisons
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()