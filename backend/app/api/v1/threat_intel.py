import uuid
from typing import Any, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.models.threat_intel import IndicatorType, IndicatorSeverity
from app.schemas.threat_intel import ThreatIndicatorCreate, ThreatIndicatorRead, ThreatIndicatorUpdate
from app.api.deps import get_current_active_user, RequirePermissions
from app.services.threat_intel_service import threat_intel_service

router = APIRouter()


@router.get("/indicators", response_model=dict)
async def list_indicators(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    type: Optional[IndicatorType] = Query(default=None),
    severity: Optional[IndicatorSeverity] = Query(default=None),
    is_active: Optional[bool] = Query(default=None),
    search: Optional[str] = Query(default=None),
    sort_by: str = Query(default="created_at"),
    sort_desc: bool = Query(default=True),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """List threat indicators with optional filters."""
    indicators, total = await threat_intel_service.get_indicators(
        db, skip=skip, limit=limit, type=type, severity=severity, 
        is_active=is_active, search=search, sort_by=sort_by, sort_desc=sort_desc
    )
    return {"total": total, "items": [ThreatIndicatorRead.model_validate(i) for i in indicators]}


@router.post("/indicators", response_model=ThreatIndicatorRead, status_code=status.HTTP_201_CREATED)
async def create_indicator(
    indicator_in: ThreatIndicatorCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Create a new threat indicator."""
    return await threat_intel_service.create_indicator(db, indicator_in=indicator_in)


@router.get("/indicators/{indicator_id}", response_model=ThreatIndicatorRead)
async def get_indicator(
    indicator_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get a specific threat indicator by ID."""
    return await threat_intel_service.get_indicator(db, indicator_id=indicator_id)


@router.patch("/indicators/{indicator_id}", response_model=ThreatIndicatorRead)
async def update_indicator(
    indicator_id: uuid.UUID,
    indicator_in: ThreatIndicatorUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Update a threat indicator."""
    return await threat_intel_service.update_indicator(db, indicator_id=indicator_id, indicator_in=indicator_in)


@router.delete("/indicators/{indicator_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_indicator(
    indicator_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RequirePermissions(["threat_intel:delete"])),
) -> None:
    """Delete a threat indicator."""
    await threat_intel_service.delete_indicator(db, indicator_id=indicator_id)
    return None
