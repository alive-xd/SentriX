from typing import List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.hunt_repository import hunt_repository
from app.models.hunt import SavedHunt
from app.schemas.hunt import SavedHuntCreate, SavedHuntUpdate
from fastapi import HTTPException
import uuid
import random

class HuntService:
    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Tuple[List[SavedHunt], int]:
        return await hunt_repository.get_multi_filtered(db, skip=skip, limit=limit)

    async def get(self, db: AsyncSession, id: str) -> Optional[SavedHunt]:
        return await hunt_repository.get(db, id=id)

    async def create(self, db: AsyncSession, *, obj_in: SavedHuntCreate) -> SavedHunt:
        return await hunt_repository.create(db, obj_in=obj_in)

    async def update(self, db: AsyncSession, *, db_obj: SavedHunt, obj_in: SavedHuntUpdate) -> SavedHunt:
        return await hunt_repository.update(db, db_obj=db_obj, obj_in=obj_in)

    async def delete(self, db: AsyncSession, *, id: str) -> SavedHunt:
        hunt = await hunt_repository.get(db, id=id)
        if not hunt:
            raise HTTPException(status_code=404, detail="Saved hunt not found")
        return await hunt_repository.remove(db, id=id)

hunt_service = HuntService()
