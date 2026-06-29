import uuid
from typing import List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models.knowledge import KnowledgeArticle, DocCategory
from app.schemas.knowledge import KnowledgeArticleCreate, KnowledgeArticleUpdate
from app.repositories.knowledge_repository import knowledge_repo

class KnowledgeService:
    async def get_articles(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 50, 
        category: Optional[DocCategory] = None, search: Optional[str] = None
    ) -> Tuple[List[KnowledgeArticle], int]:
        return await knowledge_repo.get_multi_with_filters(db, skip=skip, limit=limit, category=category, search=search)

    async def get_article(self, db: AsyncSession, article_id: uuid.UUID) -> KnowledgeArticle:
        article = await knowledge_repo.get(db, id=article_id)
        if not article: raise HTTPException(status_code=404, detail='Article not found')
        return article

    async def create_article(self, db: AsyncSession, obj_in: KnowledgeArticleCreate) -> KnowledgeArticle:
        return await knowledge_repo.create(db, obj_in=obj_in)

    async def update_article(self, db: AsyncSession, article_id: uuid.UUID, obj_in: KnowledgeArticleUpdate) -> KnowledgeArticle:
        article = await self.get_article(db, article_id)
        return await knowledge_repo.update(db, db_obj=article, obj_in=obj_in)

    async def delete_article(self, db: AsyncSession, article_id: uuid.UUID) -> None:
        article = await self.get_article(db, article_id)
        await knowledge_repo.soft_delete(db, id=article.id)

knowledge_service = KnowledgeService()
