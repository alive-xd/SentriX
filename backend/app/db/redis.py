import redis.asyncio as redis
from typing import AsyncGenerator
from app.core.config import settings

# Global Redis pool
redis_client: redis.Redis | None = None

async def init_redis_pool() -> None:
    """Initialize the Redis connection pool."""
    global redis_client
    redis_client = redis.from_url(
        settings.REDIS_URL, 
        encoding="utf-8", 
        decode_responses=True
    )

async def close_redis_pool() -> None:
    """Close the Redis connection pool."""
    global redis_client
    if redis_client:
        await redis_client.aclose()

async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    """Dependency to get Redis client in FastAPI routes."""
    if not redis_client:
        raise RuntimeError("Redis pool is not initialized")
    yield redis_client
