import uuid
from typing import Any, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.models.investigation import InvestigationStatus
from app.schemas.investigation import InvestigationCreate, InvestigationRead, InvestigationUpdate
from app.api.deps import get_current_active_user, RequirePermissions
from app.services.investigation_service import investigation_service

router = APIRouter()


@router.get("", response_model=dict)
async def list_investigations(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    status: Optional[InvestigationStatus] = Query(default=None),
    case_id: Optional[uuid.UUID] = Query(default=None),
    assigned_to_id: Optional[uuid.UUID] = Query(default=None),
    search: Optional[str] = Query(default=None),
    sort_by: str = Query(default="created_at"),
    sort_desc: bool = Query(default=True),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """List investigations with optional filters and pagination."""
    investigations, total = await investigation_service.get_investigations(
        db, skip=skip, limit=limit, status=status, case_id=case_id, 
        assigned_to_id=assigned_to_id, search=search, 
        sort_by=sort_by, sort_desc=sort_desc
    )
    return {"total": total, "items": [InvestigationRead.model_validate(inv) for inv in investigations]}


@router.post("", response_model=InvestigationRead, status_code=status.HTTP_201_CREATED)
async def create_investigation(
    investigation_in: InvestigationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Create a new investigation."""
    return await investigation_service.create_investigation(db, investigation_in=investigation_in)


@router.get("/{investigation_id}", response_model=InvestigationRead)
async def get_investigation(
    investigation_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get a specific investigation by ID."""
    return await investigation_service.get_investigation(db, investigation_id=investigation_id)


@router.patch("/{investigation_id}", response_model=InvestigationRead)
async def update_investigation(
    investigation_id: uuid.UUID,
    investigation_in: InvestigationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Update an investigation's fields."""
    return await investigation_service.update_investigation(db, investigation_id=investigation_id, investigation_in=investigation_in)


@router.delete("/{investigation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_investigation(
    investigation_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RequirePermissions(["investigation:delete"])),
) -> None:
    """Delete an investigation (Soft delete). Requires specific permissions."""
    await investigation_service.delete_investigation(db, investigation_id=investigation_id)
    return None
