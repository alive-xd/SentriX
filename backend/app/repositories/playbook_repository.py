from typing import Optional, Tuple, List
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import CRUDBase
from app.models.playbook import Playbook, PlaybookExecution, PlaybookStatus

class PlaybookRepository(CRUDBase[Playbook, dict, dict]):
    async def get_multi_with_filters(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 50,
        status: Optional[PlaybookStatus] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[Playbook], int]:
        query = select(self.model).filter(self.model.is_deleted == False)
        
        if status:
            query = query.filter(self.model.status == status)
            
        if search:
            search_filter = f'%{search}%'
            query = query.filter(
                or_(
                    self.model.name.ilike(search_filter),
                    self.model.description.ilike(search_filter)
                )
            )
            
        count_query = select(func.count()).select_from(query.subquery())
        total = await db.scalar(count_query)
        
        query = query.order_by(self.model.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        
        # Add trigger alias
        playbooks = list(result.scalars().all())
        for pb in playbooks:
            pb.trigger = pb.trigger_type
            
        return playbooks, total or 0

class PlaybookExecutionRepository(CRUDBase[PlaybookExecution, dict, dict]):
    async def get_multi_with_filters(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 50,
        playbook_name: Optional[str] = None
    ) -> Tuple[List[PlaybookExecution], int]:
        query = select(self.model).filter(self.model.is_deleted == False)
        
        if playbook_name:
            query = query.filter(self.model.playbook_name == playbook_name)
            
        count_query = select(func.count()).select_from(query.subquery())
        total = await db.scalar(count_query)
        
        query = query.order_by(self.model.started_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all()), total or 0

playbook_repo = PlaybookRepository(Playbook)
playbook_execution_repo = PlaybookExecutionRepository(PlaybookExecution)
