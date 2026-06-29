from typing import Optional, List, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import CRUDBase
from app.models.hunt import SavedHunt
from app.schemas.hunt import SavedHuntCreate, SavedHuntUpdate

class HuntRepository(CRUDBase[SavedHunt, SavedHuntCreate, SavedHuntUpdate]):
    def __init__(self):
        super().__init__(SavedHunt)

    async def get_multi_filtered(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[SavedHunt], int]:
        query = select(self.model).filter(self.model.deleted_at.is_(None))
        
        count_query = select(func.count()).select_from(query.subquery())
        total = await db.scalar(count_query)

        query = query.order_by(self.model.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        items = result.scalars().all()

        return list(items), total or 0

hunt_repository = HuntRepository()
