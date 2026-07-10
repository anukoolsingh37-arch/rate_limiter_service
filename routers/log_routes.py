from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import RateLimitLog

router = APIRouter(
    prefix="/logs",
    tags=["logs"]
)


@router.get("/", response_model=List[dict])
def get_logs(
    client_key: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(RateLimitLog)
    
    if client_key:
        query = query.filter(RateLimitLog.client_key == client_key)
    
    logs = query.order_by(RateLimitLog.timestamp.desc()).offset(skip).limit(limit).all()
    
    return [
        {
            "id": log.id,
            "client_key": log.client_key,
            "endpoint": log.endpoint,
            "allowed": bool(log.allowed),
            "timestamp": log.timestamp.isoformat(),
            "remaining_tokens": log.remaining_tokens,
            "retry_after_seconds": log.retry_after_seconds
        }
        for log in logs
    ]


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total_requests = db.query(RateLimitLog).count()
    allowed_requests = db.query(RateLimitLog).filter(RateLimitLog.allowed == 1).count()
    denied_requests = db.query(RateLimitLog).filter(RateLimitLog.allowed == 0).count()
    
    return {
        "total_requests": total_requests,
        "allowed_requests": allowed_requests,
        "denied_requests": denied_requests,
        "allow_rate": f"{(allowed_requests / total_requests * 100):.2f}%" if total_requests > 0 else "0%"
    }