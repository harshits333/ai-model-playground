from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from repositories.base import Base

class ModelResponseDB(Base):
    __tablename__ = "model_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    prompt_tokens = Column(Integer)
    completion_tokens = Column(Integer)
    total_tokens = Column(Integer)
    model = Column(String)
    cost = Column(Float)
    provider = Column(String)
    error = Column(String, nullable=True)
    latency = Column(Float)
    quality_score = Column(Float)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    comparison_id = Column(Integer, ForeignKey("comparisons.id"))
    
    comparison = relationship("Comparison", back_populates="responses")