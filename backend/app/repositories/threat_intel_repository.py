from typing import Optional, List, Tuple
from sqlalchemy import select, func, and_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import CRUDBase
from app.models.threat_intel import (
    ThreatIndicator, ThreatActor, ThreatFeed,
    IndicatorType, IndicatorSeverity
)
from app.schemas.threat_intel import (
    ThreatIndicatorCreate, ThreatIndicatorUpdate,
    ThreatActorCreate, ThreatActorUpdate,
    ThreatFeedCreate, ThreatFeedUpdate,
)


class CRUDThreatIndicator(CRUDBase[ThreatIndicator, ThreatIndicatorCreate, ThreatIndicatorUpdate]):
    async def get_multi_with_filters(
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
        
        query = select(self.model)
        filters = []
        
        if type:
            filters.append(self.model.type == type)
        if severity:
            filters.append(self.model.severity == severity)
        if is_active is not None:
            filters.append(self.model.is_active == is_active)
        if search:
            filters.append(self.model.value.ilike(f"%{search}%"))
            
        if filters:
            query = query.where(and_(*filters))

        count_result = await db.execute(select(func.count()).select_from(query.subquery()))
        total = count_result.scalar_one()
        
        sort_column = getattr(self.model, sort_by, self.model.created_at)
        if sort_desc:
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
            
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all(), total

    async def lookup_by_values(self, db: AsyncSession, values: List[str]) -> List[ThreatIndicator]:
        result = await db.execute(
            select(self.model).where(
                and_(self.model.value.in_(values), self.model.is_active)
            )
        )
        return result.scalars().all()


class CRUDThreatActor(CRUDBase[ThreatActor, ThreatActorCreate, ThreatActorUpdate]):
    pass


class CRUDThreatFeed(CRUDBase[ThreatFeed, ThreatFeedCreate, ThreatFeedUpdate]):
    pass


indicator_repo = CRUDThreatIndicator(ThreatIndicator)
actor_repo = CRUDThreatActor(ThreatActor)
feed_repo = CRUDThreatFeed(ThreatFeed)
