import time
from datetime import datetime, timezone


def get_current_timestamp() -> float:
    """Get current monotonic timestamp for rate limiting calculations."""
    return time.monotonic()


def get_utc_timestamp() -> datetime:
    """Get current UTC timestamp."""
    return datetime.now(timezone.utc)


def format_timestamp(dt: datetime) -> str:
    """Format datetime to ISO string."""
    return dt.isoformat()


def calculate_seconds_until_refill(
    current_tokens: float,
    required_tokens: float,
    refill_rate: float
) -> int:
    """Calculate seconds needed to refill required tokens."""
    import math
    missing_tokens = required_tokens - current_tokens
    if missing_tokens <= 0:
        return 0
    return math.ceil(missing_tokens / refill_rate)