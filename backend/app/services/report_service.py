from typing import List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.report_repository import report_repository
from app.models.report import Report, ReportStatus
from app.schemas.report import ReportCreate, ReportUpdate
from fastapi import HTTPException
import asyncio

class ReportService:
    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[Report], int]:
        return await report_repository.get_multi_filtered(db, skip=skip, limit=limit)

    async def get(self, db: AsyncSession, id: str) -> Optional[Report]:
        return await report_repository.get(db, id=id)

    async def create(self, db: AsyncSession, *, obj_in: ReportCreate) -> Report:
        return await report_repository.create(db, obj_in=obj_in)

    async def update(self, db: AsyncSession, *, db_obj: Report, obj_in: ReportUpdate) -> Report:
        return await report_repository.update(db, db_obj=db_obj, obj_in=obj_in)

    async def delete(self, db: AsyncSession, *, id: str) -> Report:
        report = await report_repository.get(db, id=id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        return await report_repository.remove(db, id=id)

    async def generate_report(self, db: AsyncSession, *, id: str) -> Report:
        report = await report_repository.get(db, id=id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        # Simulate report generation delay asynchronously
        # Normally this would be enqueued in Celery or similar background worker
        await asyncio.sleep(2)
        
        # Mark as completed
        update_data = ReportUpdate(
            status=ReportStatus.COMPLETED,
            file_url=f"/downloads/reports/{report.id}.pdf"
        )
        return await report_repository.update(db, db_obj=report, obj_in=update_data)

report_service = ReportService()
