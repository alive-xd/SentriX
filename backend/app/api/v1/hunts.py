from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
import asyncio
import uuid
from datetime import datetime

from app.db.session import get_db
from app.services.hunt_service import hunt_service
from app.schemas.hunt import SavedHunt, SavedHuntCreate, SavedHuntUpdate, HuntResultBase

router = APIRouter()

class HuntListResponse(BaseModel):
    items: List[SavedHunt]
    total: int
    skip: int
    limit: int

@router.get("/", response_model=HuntListResponse)
async def get_hunts(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    items, total = await hunt_service.get_multi(
        db, skip=skip, limit=limit
    )
    return {"items": items, "total": total, "skip": skip, "limit": limit}

@router.post("/", response_model=SavedHunt)
async def create_hunt(
    *,
    db: AsyncSession = Depends(get_db),
    obj_in: SavedHuntCreate,
) -> Any:
    return await hunt_service.create(db, obj_in=obj_in)

@router.patch("/{id}", response_model=SavedHunt)
async def update_hunt(
    *,
    db: AsyncSession = Depends(get_db),
    id: str,
    obj_in: SavedHuntUpdate,
) -> Any:
    hunt = await hunt_service.get(db, id=id)
    if not hunt:
        raise HTTPException(status_code=404, detail="Hunt not found")
    return await hunt_service.update(db, db_obj=hunt, obj_in=obj_in)

@router.delete("/{id}")
async def delete_hunt(
    *,
    db: AsyncSession = Depends(get_db),
    id: str,
) -> Any:
    await hunt_service.delete(db, id=id)
    return {"status": "success"}

@router.post("/execute", response_model=List[HuntResultBase])
async def execute_hunt(
    *,
    db: AsyncSession = Depends(get_db),
    query: str,
    timeRange: str
) -> Any:
    # Hunt execution logic would go here
    return []
