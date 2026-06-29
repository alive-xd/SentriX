import uuid
from typing import List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models.threat_intel import ThreatIndicator, IndicatorType, IndicatorSeverity
from app.schemas.threat_intel import ThreatIndicatorCreate, ThreatIndicatorUpdate
from app.repositories.threat_intel_repository import indicator_repo


class ThreatIntelService:
    async def get_indicators(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 50,
        type: Optional[IndicatorType] = None,
        severity: Optional[IndicatorSeverity] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
        sort_by: str = "created_at",
        sort_desc: bool = True
    ) -> Tuple[List[ThreatIndicator], int]:
        return await indicator_repo.get_multi_with_filters(
            db, skip=skip, limit=limit, type=type, severity=severity, 
            is_active=is_active, search=search, sort_by=sort_by, sort_desc=sort_desc
        )

    async def get_indicator(self, db: AsyncSession, indicator_id: uuid.UUID) -> ThreatIndicator:
        indicator = await indicator_repo.get(db, id=indicator_id)
        if not indicator:
            raise HTTPException(status_code=404, detail="Indicator not found")
        return indicator

    async def create_indicator(self, db: AsyncSession, indicator_in: ThreatIndicatorCreate) -> ThreatIndicator:
        # Simple deduplication
        existing = await indicator_repo.lookup_by_values(db, values=[indicator_in.value])
        if existing:
            raise HTTPException(status_code=400, detail="Active Indicator with this value already exists")
        return await indicator_repo.create(db, obj_in=indicator_in)

    async def update_indicator(self, db: AsyncSession, indicator_id: uuid.UUID, indicator_in: ThreatIndicatorUpdate) -> ThreatIndicator:
        indicator = await self.get_indicator(db, indicator_id)
        return await indicator_repo.update(db, db_obj=indicator, obj_in=indicator_in)

    async def delete_indicator(self, db: AsyncSession, indicator_id: uuid.UUID) -> None:
        indicator = await self.get_indicator(db, indicator_id)
        await indicator_repo.remove(db, id=indicator.id)


threat_intel_service = ThreatIntelService()
