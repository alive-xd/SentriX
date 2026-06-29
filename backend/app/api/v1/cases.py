import uuid
from typing import Any, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.models.case import CaseStatus, CaseSeverity
from app.schemas.case import CaseCreate, CaseRead, CaseUpdate
from app.schemas.case_activity import CaseCommentCreate, CaseCommentRead
from app.api.deps import get_current_active_user, RequirePermissions
from app.services.case_service import case_service

router = APIRouter()


@router.get("", response_model=dict)
async def list_cases(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    status: Optional[CaseStatus] = Query(default=None),
    severity: Optional[CaseSeverity] = Query(default=None),
    assigned_to_id: Optional[uuid.UUID] = Query(default=None),
    search: Optional[str] = Query(default=None),
    sort_by: str = Query(default="created_at"),
    sort_desc: bool = Query(default=True),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """List cases with optional filters and pagination."""
    cases, total = await case_service.get_cases(
        db, skip=skip, limit=limit, status=status, severity=severity, 
        assigned_to_id=assigned_to_id, search=search, 
        sort_by=sort_by, sort_desc=sort_desc
    )
    return {"total": total, "items": [CaseRead.model_validate(c) for c in cases]}


@router.post("", response_model=CaseRead, status_code=status.HTTP_201_CREATED)
async def create_case(
    case_in: CaseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Create a new case."""
    return await case_service.create_case(db, case_in=case_in, current_user=current_user)


@router.get("/{case_id}", response_model=CaseRead)
async def get_case(
    case_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get a specific case by ID."""
    return await case_service.get_case(db, case_id=case_id)


@router.patch("/{case_id}", response_model=CaseRead)
async def update_case(
    case_id: uuid.UUID,
    case_in: CaseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Update a case's fields."""
    return await case_service.update_case(db, case_id=case_id, case_in=case_in, current_user=current_user)


@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_case(
    case_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RequirePermissions(["case:delete"])),
) -> None:
    """Delete a case (Soft delete). Requires specific permissions."""
    await case_service.delete_case(db, case_id=case_id)
    return None


@router.post("/{case_id}/comments", response_model=CaseCommentRead, status_code=status.HTTP_201_CREATED)
async def add_case_comment(
    case_id: uuid.UUID,
    comment_in: CaseCommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Add a comment to a case."""
    return await case_service.add_comment(db, case_id=case_id, obj_in=comment_in, current_user=current_user)
