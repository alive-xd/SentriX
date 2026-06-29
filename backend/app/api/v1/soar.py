from typing import Any, Optional
import uuid
from fastapi import APIRouter, Depends, Query, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.playbook import PlaybookStatus
from app.schemas.playbook import PlaybookRead, PlaybookCreate, PlaybookUpdate, PlaybookExecutionRead
from app.services.playbook_service import playbook_service

router = APIRouter()

@router.get('/playbooks')
async def list_playbooks(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    playbook_status: Optional[PlaybookStatus] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    items, total = await playbook_service.get_playbooks(db, skip=skip, limit=limit, status=playbook_status, search=search)
    return {'items': items, 'total': total, 'skip': skip, 'limit': limit}

@router.post('/playbooks', response_model=PlaybookRead, status_code=status.HTTP_201_CREATED)
async def create_playbook(
    *,
    db: AsyncSession = Depends(get_db),
    playbook_in: PlaybookCreate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    return await playbook_service.create_playbook(db, obj_in=playbook_in)

@router.get('/playbooks/{playbook_id}', response_model=PlaybookRead)
async def get_playbook(
    playbook_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    return await playbook_service.get_playbook(db, playbook_id)

@router.patch('/playbooks/{playbook_id}', response_model=PlaybookRead)
async def update_playbook(
    playbook_id: uuid.UUID,
    playbook_in: PlaybookUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    return await playbook_service.update_playbook(db, playbook_id, playbook_in)

@router.delete('/playbooks/{playbook_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_playbook(
    playbook_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> None:
    await playbook_service.delete_playbook(db, playbook_id)

@router.get('/executions')
async def list_executions(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    playbook_name: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    items, total = await playbook_service.get_executions(db, skip=skip, limit=limit, playbook_name=playbook_name)
    return {'items': items, 'total': total, 'skip': skip, 'limit': limit}
