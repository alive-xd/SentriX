import uuid
from typing import Any, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.models.alert import AlertStatus, AlertSeverity
from app.schemas.alert import AlertCreate, AlertRead, AlertUpdate, AlertPromote
from app.schemas.case import CaseRead
from app.api.deps import get_current_active_user, RequirePermissions
from app.services.alert_service import alert_service
from app.services.case_service import case_service

router = APIRouter()


@router.get("", response_model=dict)
async def list_alerts(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    status: Optional[AlertStatus] = Query(default=None),
    severity: Optional[AlertSeverity] = Query(default=None),
    case_id: Optional[uuid.UUID] = Query(default=None),
    assigned_to_id: Optional[uuid.UUID] = Query(default=None),
    search: Optional[str] = Query(default=None),
    sort_by: str = Query(default="created_at"),
    sort_desc: bool = Query(default=True),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """List alerts with optional filters and pagination."""
    alerts, total = await alert_service.get_alerts(
        db, skip=skip, limit=limit, status=status, severity=severity, 
        case_id=case_id, assigned_to_id=assigned_to_id, 
        search=search, sort_by=sort_by, sort_desc=sort_desc
    )
    return {"total": total, "items": [AlertRead.model_validate(a) for a in alerts]}


@router.post("", response_model=AlertRead, status_code=status.HTTP_201_CREATED)
async def create_alert(
    alert_in: AlertCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Create a new alert (e.g., from an integration or manual entry)."""
    return await alert_service.create_alert(db, alert_in=alert_in)


@router.get("/{alert_id}", response_model=AlertRead)
async def get_alert(
    alert_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get a specific alert by ID."""
    return await alert_service.get_alert(db, alert_id=alert_id)


@router.patch("/{alert_id}", response_model=AlertRead)
async def update_alert(
    alert_id: uuid.UUID,
    alert_in: AlertUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Update an alert's fields."""
    return await alert_service.update_alert(db, alert_id=alert_id, alert_in=alert_in)


@router.post("/{alert_id}/promote", response_model=CaseRead)
async def promote_alert_to_case(
    alert_id: uuid.UUID,
    promote_in: AlertPromote,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Promote an alert into a new case or link it to an existing case."""
    return await case_service.promote_alert(db, alert_id=alert_id, promote_in=promote_in, current_user=current_user)


@router.post("/{alert_id}/assign", response_model=AlertRead)
async def assign_alert(
    alert_id: uuid.UUID,
    user_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Assign an alert to a specific user."""
    return await alert_service.assign_alert(db, alert_id=alert_id, user_id=user_id)


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert(
    alert_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RequirePermissions(["alert:delete"])),
) -> None:
    """Delete an alert (Soft delete). Requires specific permissions."""
    await alert_service.delete_alert(db, alert_id=alert_id)
    return None
