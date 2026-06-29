import uuid
from typing import List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models.investigation import Investigation, InvestigationStatus
from app.schemas.investigation import InvestigationCreate, InvestigationUpdate
from app.repositories.investigation_repository import investigation_repo


class InvestigationService:
    async def get_investigations(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 50,
        status: Optional[InvestigationStatus] = None,
        case_id: Optional[uuid.UUID] = None,
        assigned_to_id: Optional[uuid.UUID] = None,
        search: Optional[str] = None,
        sort_by: str = "created_at",
        sort_desc: bool = True
    ) -> Tuple[List[Investigation], int]:
        return await investigation_repo.get_multi_with_filters(
            db, skip=skip, limit=limit, status=status,
            case_id=case_id, assigned_to_id=assigned_to_id, 
            search=search, sort_by=sort_by, sort_desc=sort_desc
        )

    async def get_investigation(self, db: AsyncSession, investigation_id: uuid.UUID) -> Investigation:
        investigation = await investigation_repo.get(db, id=investigation_id)
        if not investigation:
            raise HTTPException(status_code=404, detail="Investigation not found")
        return investigation

    async def create_investigation(self, db: AsyncSession, investigation_in: InvestigationCreate) -> Investigation:
        return await investigation_repo.create(db, obj_in=investigation_in)

    async def update_investigation(
        self, db: AsyncSession, investigation_id: uuid.UUID, investigation_in: InvestigationUpdate
    ) -> Investigation:
        investigation = await self.get_investigation(db, investigation_id)
        return await investigation_repo.update(db, db_obj=investigation, obj_in=investigation_in)

    async def delete_investigation(self, db: AsyncSession, investigation_id: uuid.UUID) -> None:
        investigation = await self.get_investigation(db, investigation_id)
        await investigation_repo.soft_delete(db, id=investigation.id)


investigation_service = InvestigationService()
