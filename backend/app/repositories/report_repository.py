from typing import List, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import CRUDBase
from app.models.report import Report
from app.schemas.report import ReportCreate, ReportUpdate

class ReportRepository(CRUDBase[Report, ReportCreate, ReportUpdate]):
    def __init__(self):
        super().__init__(Report)

    async def get_multi_filtered(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[Report], int]:
        query = select(self.model).filter(self.model.deleted_at.is_(None))
        
        count_query = select(func.count()).select_from(query.subquery())
        total = await db.scalar(count_query)

        query = query.order_by(self.model.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        items = result.scalars().all()

        return list(items), total or 0

report_repository = ReportRepository()
