import uuid
from typing import Any, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.models.asset import AssetType, AssetCriticality, AssetStatus
from app.schemas.asset import AssetCreate, AssetRead, AssetUpdate, VulnerabilityCreate, VulnerabilityRead, AssetStats
from app.api.deps import get_current_active_user, RequirePermissions
from app.services.asset_service import asset_service

router = APIRouter()


@router.get("/stats", response_model=AssetStats)
async def get_asset_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get high-level statistics about assets."""
    return await asset_service.get_stats(db)


@router.get("", response_model=dict)
async def list_assets(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    search: Optional[str] = Query(default=None),
    asset_type: Optional[AssetType] = Query(default=None),
    criticality: Optional[AssetCriticality] = Query(default=None),
    status: Optional[AssetStatus] = Query(default=None),
    sort_by: str = Query(default="risk_score"),
    sort_desc: bool = Query(default=True),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """List assets with filtering, pagination, and sorting."""
    assets, total = await asset_service.get_assets(
        db, skip=skip, limit=limit, search=search,
        asset_type=asset_type, criticality=criticality, status=status,
        sort_by=sort_by, sort_desc=sort_desc
    )
    return {"total": total, "items": [AssetRead.model_validate(a) for a in assets]}


@router.post("", response_model=AssetRead, status_code=status.HTTP_201_CREATED)
async def create_asset(
    asset_in: AssetCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Create a new asset."""
    return await asset_service.create_asset(db, asset_in=asset_in)


@router.get("/{asset_id}", response_model=AssetRead)
async def get_asset(
    asset_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get a specific asset by ID."""
    return await asset_service.get_asset(db, asset_id=asset_id)


@router.patch("/{asset_id}", response_model=AssetRead)
async def update_asset(
    asset_id: uuid.UUID,
    asset_in: AssetUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Update an asset's information."""
    return await asset_service.update_asset(db, asset_id=asset_id, asset_in=asset_in)


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(
    asset_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(RequirePermissions(["asset:delete"])),
) -> None:
    """Soft delete an asset."""
    await asset_service.delete_asset(db, asset_id=asset_id)
    return None


@router.post("/{asset_id}/vulnerabilities", response_model=VulnerabilityRead, status_code=status.HTTP_201_CREATED)
async def add_vulnerability(
    asset_id: uuid.UUID,
    vuln_in: VulnerabilityCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Add a new vulnerability to an asset."""
    return await asset_service.add_vulnerability(db, asset_id=asset_id, vuln_in=vuln_in)
