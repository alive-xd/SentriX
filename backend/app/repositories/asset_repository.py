from typing import Optional, List, Tuple
from sqlalchemy import select, func, and_, or_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.repositories.base import CRUDBase
from app.models.asset import Asset, AssetVulnerability, AssetType, AssetCriticality, AssetStatus
from app.schemas.asset import AssetCreate, AssetUpdate, VulnerabilityCreate, AssetStats


class CRUDAsset(CRUDBase[Asset, AssetCreate, AssetUpdate]):
    async def get_by_hostname(self, db: AsyncSession, hostname: str) -> Optional[Asset]:
        result = await db.execute(select(self.model).where(self.model.hostname == hostname))
        return result.scalars().first()

    async def get_multi_with_filters(
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
        query = select(self.model)
        filters = []
        
        if search:
            filters.append(
                or_(self.model.hostname.ilike(f"%{search}%"), self.model.ip_address.ilike(f"%{search}%"))
            )
        if asset_type:
            filters.append(self.model.asset_type == asset_type)
        if criticality:
            filters.append(self.model.criticality == criticality)
        if status:
            filters.append(self.model.status == status)
            
        if filters:
            query = query.where(and_(*filters))

        count_result = await db.execute(select(func.count()).select_from(query.subquery()))
        total = count_result.scalar_one()

        sort_column = getattr(self.model, sort_by, self.model.risk_score)
        if sort_desc:
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
            
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all(), total

    async def get_stats(self, db: AsyncSession) -> AssetStats:
        total = (await db.execute(select(func.count()).select_from(self.model))).scalar_one()
        active = (await db.execute(select(func.count()).where(self.model.status == AssetStatus.ACTIVE))).scalar_one()
        critical = (await db.execute(select(func.count()).where(self.model.criticality == AssetCriticality.CRITICAL))).scalar_one()
        high_risk = (await db.execute(select(func.count()).where(self.model.risk_score > 70))).scalar_one()
        return AssetStats(total=total, active=active, critical=critical, high_risk_count=high_risk)

    async def add_vulnerability(
        self, db: AsyncSession, asset_id: uuid.UUID, obj_in: VulnerabilityCreate
    ) -> AssetVulnerability:
        vuln = AssetVulnerability(asset_id=asset_id, **obj_in.model_dump())
        db.add(vuln)
        await db.commit()
        await db.refresh(vuln)
        return vuln


asset_repo = CRUDAsset(Asset)
