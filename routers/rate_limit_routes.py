from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import RateLimitCheckRequest, RateLimitCheckResponse
from app.database import get_db
from app.models import RateLimitLog
from services.token_bucket_service import TokenBucketService

router = APIRouter(
    prefix="/rate-limit",
    tags=["rate-limit"]
)

# Global token bucket service instance
token_bucket_service = TokenBucketService()


@router.post("/check", response_model=RateLimitCheckResponse)
def check_rate_limit(request: RateLimitCheckRequest, db: Session = Depends(get_db)):
    try:
        result = token_bucket_service.check_rate_limit(
            client_key=request.client_key,
            endpoint=request.endpoint
        )
        
        # Log the request
        log = RateLimitLog(
            client_key=request.client_key,
            endpoint=request.endpoint,
            allowed=1 if result["allowed"] else 0,
            remaining_tokens=result["remaining_tokens"],
            retry_after_seconds=result["retry_after_seconds"]
        )
        db.add(log)
        db.commit()
        
        return result
        
    except KeyError:
        raise HTTPException(status_code=404, detail="Client not found")