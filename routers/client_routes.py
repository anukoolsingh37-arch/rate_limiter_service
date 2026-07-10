from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import ClientCreate
from app.database import get_db
from app.models import Client
from services.token_bucket_service import TokenBucketService

router = APIRouter(
    prefix="/clients",
    tags=["clients"]
)

# Global token bucket service instance
token_bucket_service = TokenBucketService()


@router.post("/", status_code=201)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    # Check if client already exists
    existing_client = db.query(Client).filter(Client.client_key == client.client_key).first()
    if existing_client:
        raise HTTPException(status_code=400, detail="Client already exists")
    
    # Create in database
    db_client = Client(
        client_key=client.client_key,
        capacity=client.capacity,
        refill_rate_per_second=client.refill_rate_per_second
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    
    # Create in token bucket service
    result = token_bucket_service.create_client(
        client_key=client.client_key,
        capacity=client.capacity,
        refill_rate_per_second=client.refill_rate_per_second
    )
    
    return result


@router.get("/")
def get_clients(db: Session = Depends(get_db)):
    # Get from token bucket service (in-memory state)
    return token_bucket_service.get_all_clients()


@router.get("/{client_key}")
def get_client(client_key: str, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.client_key == client_key).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Get current token state
    if client_key in token_bucket_service.buckets:
        bucket = token_bucket_service.buckets[client_key]
        return {
            "client_key": client.client_key,
            "capacity": client.capacity,
            "refill_rate_per_second": client.refill_rate_per_second,
            "current_tokens": int(bucket.tokens)
        }
    
    return {
        "client_key": client.client_key,
        "capacity": client.capacity,
        "refill_rate_per_second": client.refill_rate_per_second,
        "current_tokens": client.capacity
    }