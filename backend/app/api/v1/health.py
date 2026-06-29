from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from redis.asyncio import Redis
import logging

from app.db.session import get_db
from app.db.redis import get_redis

router = APIRouter()
logger = logging.getLogger("sentrix")


@router.get("/health", tags=["Health"])
async def health_check():
    """Basic health check that the API is running."""
    return {"status": "ok", "version": "1.0.0"}


@router.get("/ready", tags=["Health"])
async def readiness_check(
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis)
):
    """
    Readiness check that verifies connections to dependencies:
    - Postgres DB
    - Redis
    """
    db_status = "ok"
    redis_status = "ok"

    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(f"Database readiness check failed: {e}")
        db_status = "error"

    try:
        await redis.ping()
    except Exception as e:
        logger.error(f"Redis readiness check failed: {e}")
        redis_status = "error"

    status_code = 200 if db_status == "ok" and redis_status == "ok" else 503

    return {
        "status": "ready" if status_code == 200 else "not_ready",
        "dependencies": {
            "database": db_status,
            "redis": redis_status
        }
    }


@router.get("/live", tags=["Health"])
async def liveness_check():
    """Liveness check for container orchestration."""
    return {"status": "alive"}
