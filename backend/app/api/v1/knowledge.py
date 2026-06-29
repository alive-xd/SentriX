from typing import Any, Optional
import uuid
from fastapi import APIRouter, Depends, Query, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.knowledge import DocCategory
from app.schemas.knowledge import KnowledgeArticleRead, KnowledgeArticleCreate, KnowledgeArticleUpdate

from app.services.knowledge_service import knowledge_service

router = APIRouter()

@router.get("")
async def list_articles(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category: Optional[DocCategory] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    items, total = await knowledge_service.get_articles(db, skip=skip, limit=limit, category=category, search=search)
    return {"items": items, "total": total, "skip": skip, "limit": limit}

@router.post("", response_model=KnowledgeArticleRead, status_code=status.HTTP_201_CREATED)
async def create_article(
    *,
    db: AsyncSession = Depends(get_db),
    article_in: KnowledgeArticleCreate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    return await knowledge_service.create_article(db, obj_in=article_in)

@router.get("/{article_id}", response_model=KnowledgeArticleRead)
async def get_article(
    article_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    return await knowledge_service.get_article(db, article_id)

@router.patch("/{article_id}", response_model=KnowledgeArticleRead)
async def update_article(
    article_id: uuid.UUID,
    article_in: KnowledgeArticleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    return await knowledge_service.update_article(db, article_id, obj_in=article_in)

@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_article(
    article_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> None:
    await knowledge_service.delete_article(db, article_id)
