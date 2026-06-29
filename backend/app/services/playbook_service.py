import uuid
from typing import List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models.playbook import Playbook, PlaybookExecution, PlaybookStatus
from app.schemas.playbook import PlaybookCreate, PlaybookUpdate
from app.repositories.playbook_repository import playbook_repo, playbook_execution_repo

class PlaybookService:
    async def get_playbooks(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 50, 
        status: Optional[PlaybookStatus] = None, search: Optional[str] = None
    ) -> Tuple[List[Playbook], int]:
        return await playbook_repo.get_multi_with_filters(db, skip=skip, limit=limit, status=status, search=search)

    async def get_playbook(self, db: AsyncSession, playbook_id: uuid.UUID) -> Playbook:
        playbook = await playbook_repo.get(db, id=playbook_id)
        if not playbook: raise HTTPException(status_code=404, detail='Playbook not found')
        playbook.trigger = playbook.trigger_type
        return playbook

    async def create_playbook(self, db: AsyncSession, obj_in: PlaybookCreate) -> Playbook:
        playbook = await playbook_repo.create(db, obj_in=obj_in)
        playbook.trigger = playbook.trigger_type
        return playbook

    async def update_playbook(self, db: AsyncSession, playbook_id: uuid.UUID, obj_in: PlaybookUpdate) -> Playbook:
        playbook = await self.get_playbook(db, playbook_id)
        playbook = await playbook_repo.update(db, db_obj=playbook, obj_in=obj_in)
        playbook.trigger = playbook.trigger_type
        return playbook

    async def delete_playbook(self, db: AsyncSession, playbook_id: uuid.UUID) -> None:
        playbook = await self.get_playbook(db, playbook_id)
        await playbook_repo.soft_delete(db, id=playbook.id)

    async def get_executions(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 50, playbook_name: Optional[str] = None
    ) -> Tuple[List[PlaybookExecution], int]:
        return await playbook_execution_repo.get_multi_with_filters(db, skip=skip, limit=limit, playbook_name=playbook_name)

playbook_service = PlaybookService()
