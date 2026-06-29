import uuid
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.models.detection import RuleStatus, RuleSeverity, RuleType
from app.repositories.detection_repository import detection_repo
from app.schemas.detection import (
    DetectionRuleCreate, DetectionRuleRead, DetectionRuleUpdate,
    DetectionRuleStats, RuleTestCreate, RuleTestRead,
)
from app.services.auth_service import get_current_user

router = APIRouter()


@router.get("/stats", response_model=DetectionRuleStats)
async def get_detection_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Aggregated statistics for the detection engineering dashboard."""
    return await detection_repo.get_stats(db)


@router.get("", response_model=dict)
async def list_rules(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    status: Optional[RuleStatus] = Query(default=None),
    severity: Optional[RuleSeverity] = Query(default=None),
    rule_type: Optional[RuleType] = Query(default=None),
    search: Optional[str] = Query(default=None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """List detection rules with filtering and pagination."""
    rules, total = await detection_repo.get_multi(
        db, skip=skip, limit=limit,
        status=status, severity=severity, rule_type=rule_type, search=search,
    )
    return {"total": total, "items": [DetectionRuleRead.model_validate(r) for r in rules]}


@router.post("", response_model=DetectionRuleRead, status_code=status.HTTP_201_CREATED)
async def create_rule(
    rule_in: DetectionRuleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Create a new detection rule."""
    return await detection_repo.create(db, obj_in=rule_in, created_by_id=current_user.id)


@router.get("/{rule_id}", response_model=DetectionRuleRead)
async def get_rule(
    rule_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get a specific detection rule by ID."""
    rule = await detection_repo.get_by_id(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Detection rule not found")
    return rule


@router.patch("/{rule_id}", response_model=DetectionRuleRead)
async def update_rule(
    rule_id: uuid.UUID,
    rule_in: DetectionRuleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Update a detection rule."""
    rule = await detection_repo.get_by_id(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Detection rule not found")
    return await detection_repo.update(db, db_obj=rule, obj_in=rule_in, modified_by_id=current_user.id)


@router.delete("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rule(
    rule_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a detection rule."""
    rule = await detection_repo.get_by_id(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Detection rule not found")
    await detection_repo.delete(db, db_obj=rule)


@router.post("/{rule_id}/activate", response_model=DetectionRuleRead)
async def activate_rule(
    rule_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Activate a detection rule (mark as ACTIVE and enable)."""
    rule = await detection_repo.get_by_id(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Detection rule not found")
    return await detection_repo.activate(db, db_obj=rule, user_id=current_user.id)


@router.post("/{rule_id}/deactivate", response_model=DetectionRuleRead)
async def deactivate_rule(
    rule_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Deactivate a detection rule."""
    rule = await detection_repo.get_by_id(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Detection rule not found")
    return await detection_repo.deactivate(db, db_obj=rule, user_id=current_user.id)


@router.post("/{rule_id}/tests", response_model=RuleTestRead, status_code=status.HTTP_201_CREATED)
async def record_test_run(
    rule_id: uuid.UUID,
    test_in: RuleTestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """Record the result of a test run for a detection rule."""
    rule = await detection_repo.get_by_id(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Detection rule not found")
    return await detection_repo.add_test_run(db, rule_id=rule_id, ran_by_id=current_user.id, obj_in=test_in)
