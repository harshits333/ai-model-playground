from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from repositories.base import Base

class Comparison(Base):
    __tablename__ = "comparisons"
    
    id = Column(Integer, primary_key=True, index=True)
    user_prompt = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    responses = relationship("ModelResponseDB", back_populates="comparison")