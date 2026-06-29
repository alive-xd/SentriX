from typing import Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.schemas.alert import AlertRead
from app.schemas.case import CaseRead
from app.services.auth_service import get_current_user
from app.services.dashboard_service import dashboard_service

router = APIRouter()


@router.get("/summary")
async def get_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Top-level KPI metrics:
    - Open/in-progress case counts
    - New/critical alert counts
    - Asset totals
    - Active detection rules
    - Active IoC count
    """
    return await dashboard_service.get_summary(db)


@router.get("/severity-breakdown")
async def get_severity_breakdown(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Case and alert distribution grouped by severity level."""
    return await dashboard_service.get_severity_breakdown(db)


@router.get("/recent-alerts", response_model=list[AlertRead])
async def get_recent_alerts(
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Most recent unacknowledged alerts for the dashboard feed."""
    return await dashboard_service.get_recent_alerts(db, limit=limit)


@router.get("/activity-feed", response_model=list[CaseRead])
async def get_activity_feed(
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Recently updated cases for the SOC activity stream."""
    return await dashboard_service.get_activity_feed(db, limit=limit)
