import pytest
from services.token_bucket_service import TokenBucketService


def test_create_client():
    service = TokenBucketService()
    result = service.create_client(
        client_key="test_user",
        capacity=5,
        refill_rate_per_second=1.0
    )
    
    assert result["client_key"] == "test_user"
    assert result["capacity"] == 5
    assert result["refill_rate_per_second"] == 1.0
    assert "test_user" in service.client_rules
    assert "test_user" in service.buckets


def test_get_all_clients():
    service = TokenBucketService()
    service.create_client("user1", 10, 2.0)
    service.create_client("user2", 20, 3.0)
    
    clients = service.get_all_clients()
    
    assert len(clients) == 2
    client_keys = [c["client_key"] for c in clients]
    assert "user1" in client_keys
    assert "user2" in client_keys


def test_rate_limit_allows_request():
    service = TokenBucketService()
    service.create_client("test_user", 5, 1.0)
    
    result = service.check_rate_limit("test_user", "/api/test")
    
    assert result["allowed"] is True
    assert result["remaining_tokens"] == 4


def test_rate_limit_denies_request():
    service = TokenBucketService()
    service.create_client("test_user", 2, 1.0)
    
    # Use up all tokens
    service.check_rate_limit("test_user", "/api/test")
    service.check_rate_limit("test_user", "/api/test")
    
    # This should be denied
    result = service.check_rate_limit("test_user", "/api/test")
    
    assert result["allowed"] is False
    assert result["retry_after_seconds"] > 0


def test_rate_limit_client_not_found():
    service = TokenBucketService()
    
    with pytest.raises(KeyError):
        service.check_rate_limit("nonexistent", "/api/test")


def test_token_refill():
    import time
    service = TokenBucketService()
    service.create_client("test_user", 5, 10.0)  # 10 tokens per second
    
    # Use up all tokens
    for _ in range(5):
        service.check_rate_limit("test_user", "/api/test")
    
    # Wait for refill
    time.sleep(0.5)
    
    # Should have refilled ~5 tokens
    result = service.check_rate_limit("test_user", "/api/test")
    assert result["allowed"] is True