from pydantic import BaseModel, Field


class ClientCreate(BaseModel):
    client_key: str = Field(..., example="user_123")
    capacity: int = Field(..., gt=0, example=5)
    refill_rate_per_second: float = Field(...,gt=0, example=1)


class RateLimitCheckRequest(BaseModel):
    client_key: str = Field(..., example="user_123")
    endpoint: str = Field(..., example="/api/products")


class RateLimitCheckResponse(BaseModel):
    allowed:bool
    client_key: str
    endpoint: str
    limit: int
    remaining_tokens: int
    retry_after_seconds: int
    message:str