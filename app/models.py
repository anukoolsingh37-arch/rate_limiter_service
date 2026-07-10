from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base
from datetime import datetime


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    client_key = Column(String, unique=True, index=True)
    capacity = Column(Integer)
    refill_rate_per_second = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class RateLimitLog(Base):
    __tablename__ = "rate_limit_logs"

    id = Column(Integer, primary_key=True, index=True)
    client_key = Column(String, index=True)
    endpoint = Column(String)
    allowed = Column(Integer)  # 1 for allowed, 0 for denied
    timestamp = Column(DateTime, default=datetime.utcnow)
    remaining_tokens = Column(Integer)
    retry_after_seconds = Column(Integer, nullable=True)