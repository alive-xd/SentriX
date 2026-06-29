import uuid
from typing import List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models.asset import Asset, AssetType, AssetCriticality, AssetStatus, AssetVulnerability
from app.schemas.asset import AssetCreate, AssetUpdate, VulnerabilityCreate, AssetStats
from app.repositories.asset_repository import asset_repo


class AssetService:
    async def get_assets(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 50,
        search: Optional[str] = None,
        asset_type: Optional[AssetType] = None,
        criticality: Optional[AssetCriticality] = None,
        status: Optional[AssetStatus] = None,
        sort_by: str = "risk_score",
        sort_desc: bool = True
    ) -> Tuple[List[Asset], int]:
        return await asset_repo.get_multi_with_filters(
            db, skip=skip, limit=limit, search=search,
            asset_type=asset_type, criticality=criticality, status=status,
            sort_by=sort_by, sort_desc=sort_desc
        )

    async def get_asset(self, db: AsyncSession, asset_id: uuid.UUID) -> Asset:
        asset = await asset_repo.get(db, id=asset_id)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        return asset

    async def create_asset(self, db: AsyncSession, asset_in: AssetCreate) -> Asset:
        existing_asset = await asset_repo.get_by_hostname(db, hostname=asset_in.hostname)
        if existing_asset:
            raise HTTPException(status_code=400, detail="Asset with this hostname already exists")
        return await asset_repo.create(db, obj_in=asset_in)

    async def update_asset(self, db: AsyncSession, asset_id: uuid.UUID, asset_in: AssetUpdate) -> Asset:
        asset = await self.get_asset(db, asset_id)
        if asset_in.hostname and asset_in.hostname != asset.hostname:
            existing_asset = await asset_repo.get_by_hostname(db, hostname=asset_in.hostname)
            if existing_asset:
                raise HTTPException(status_code=400, detail="Asset with this hostname already exists")
        return await asset_repo.update(db, db_obj=asset, obj_in=asset_in)

    async def delete_asset(self, db: AsyncSession, asset_id: uuid.UUID) -> None:
        asset = await self.get_asset(db, asset_id)
        await asset_repo.soft_delete(db, id=asset.id)

    async def add_vulnerability(self, db: AsyncSession, asset_id: uuid.UUID, vuln_in: VulnerabilityCreate) -> AssetVulnerability:
        asset = await self.get_asset(db, asset_id)
        
        vuln = await asset_repo.add_vulnerability(db, asset_id=asset.id, obj_in=vuln_in)
        
        # Simple risk score update logic: Criticality + base score sum, max 100
        new_risk = asset.risk_score + (vuln_in.base_score * 2.0)
        new_risk = min(new_risk, 100.0)
        
        await asset_repo.update(db, db_obj=asset, obj_in=AssetUpdate(risk_score=new_risk))
        
        return vuln
        
    async def get_stats(self, db: AsyncSession) -> AssetStats:
        return await asset_repo.get_stats(db)


asset_service = AssetService()
