from typing import Optional, Tuple, List
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import CRUDBase
from app.models.knowledge import KnowledgeArticle, DocCategory

class KnowledgeRepository(CRUDBase[KnowledgeArticle, dict, dict]):
    async def get_multi_with_filters(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 50,
        category: Optional[DocCategory] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[KnowledgeArticle], int]:
        query = select(self.model).filter(self.model.is_deleted == False)
        
        if category:
            query = query.filter(self.model.category == category)
            
        if search:
            search_filter = f'%{search}%'
            query = query.filter(
                or_(
                    self.model.title.ilike(search_filter),
                    self.model.description.ilike(search_filter)
                )
            )
            
        # Count
        count_query = select(func.count()).select_from(query.subquery())
        total = await db.scalar(count_query)
        
        # Paginate
        query = query.order_by(self.model.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all()), total or 0

knowledge_repo = KnowledgeRepository(KnowledgeArticle)
