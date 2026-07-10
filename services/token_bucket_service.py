import time
import math
from dataclasses import dataclass
from threading import Lock


@dataclass
class ClientRule:
    client_key: str
    capacity: int
    refill_rate_per_second: float


@dataclass
class BucketState:
    tokens: float
    last_refill_time: float


class TokenBucketService:
    def __init__(self):
        self.client_rules = {}
        self.buckets = {}
        self.lock = Lock()

    def create_client(self, client_key: str, capacity: int, refill_rate_per_second: float):
        rule = ClientRule(
            client_key=client_key,
            capacity=capacity,
            refill_rate_per_second=refill_rate_per_second
        )

        bucket = BucketState(
            tokens=capacity,
            last_refill_time=time.monotonic()
        )

        self.client_rules[client_key] = rule
        self.buckets[client_key] = bucket

        return {
            "message": "Client created successfully",
            "client_key": client_key,
            "capacity": capacity,
            "refill_rate_per_second": refill_rate_per_second
        }

    def get_all_clients(self):
        clients = []

        for client_key, rule in self.client_rules.items():
            bucket = self.buckets[client_key]

            clients.append({
                "client_key": client_key,
                "capacity": rule.capacity,
                "refill_rate_per_second": rule.refill_rate_per_second,
                "current_tokens": int(bucket.tokens)
            })

        return clients

    def check_rate_limit(self, client_key: str, endpoint: str):
        with self.lock:
            if client_key not in self.client_rules:
                raise KeyError("Client not found")

            rule = self.client_rules[client_key]
            bucket = self.buckets[client_key]

            current_time = time.monotonic()

            time_passed = current_time - bucket.last_refill_time

            tokens_to_add = time_passed * rule.refill_rate_per_second

            bucket.tokens = min(
                rule.capacity,
                bucket.tokens + tokens_to_add
            )

            bucket.last_refill_time = current_time

            if bucket.tokens >= 1:
                bucket.tokens -= 1

                return {
                    "allowed": True,
                    "client_key": client_key,
                    "endpoint": endpoint,
                    "limit": rule.capacity,
                    "remaining_tokens": int(bucket.tokens),
                    "retry_after_seconds": 0,
                    "message": "Request allowed"
                }

            missing_tokens = 1 - bucket.tokens
            retry_after_seconds = math.ceil(
                missing_tokens / rule.refill_rate_per_second
            )
            return {
                "allowed": False,
                "client_key": client_key,
                "endpoint": endpoint,
                "limit": rule.capacity,
                "remaining_tokens": int(bucket.tokens),
                "retry_after_seconds": retry_after_seconds,
                "message": "Rate limit exceeded"
            }