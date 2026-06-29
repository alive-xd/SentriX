from typing import Optional, List, Tuple
from sqlalchemy import select, func, and_, or_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.repositories.base import CRUDBase
from app.models.case import Case, CaseSeverity, CaseStatus
from app.models.case_activity import CaseComment, CaseTimeline, TimelineEventType
from app.schemas.case import CaseCreate, CaseUpdate
from app.schemas.case_activity import CaseCommentCreate


class CRUDCase(CRUDBase[Case, CaseCreate, CaseUpdate]):
    async def get_multi_with_filters(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 50,
        status: Optional[CaseStatus] = None,
        severity: Optional[CaseSeverity] = None,
        assigned_to_id: Optional[uuid.UUID] = None,
        search: Optional[str] = None,
        sort_by: str = "created_at",
        sort_desc: bool = True
    ) -> Tuple[List[Case], int]:
        
        query = select(self.model)
        filters = []
        
        if status:
            filters.append(self.model.status == status)
        if severity:
            filters.append(self.model.severity == severity)
        if assigned_to_id:
            filters.append(self.model.assigned_to_id == assigned_to_id)
        if search:
            filters.append(
                or_(
                    self.model.title.ilike(f"%{search}%"),
                    self.model.description.ilike(f"%{search}%"),
                )
            )
            
        if filters:
            query = query.where(and_(*filters))
            
        count_result = await db.execute(select(func.count()).select_from(query.subquery()))
        total = count_result.scalar_one()
        
        sort_column = getattr(self.model, sort_by, self.model.created_at)
        if sort_desc:
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
            
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all(), total

    async def create_with_author(
        self, db: AsyncSession, obj_in: CaseCreate, created_by_id: uuid.UUID
    ) -> Case:
        db_obj = Case(
            **obj_in.model_dump(exclude={"assigned_to_id"}),
            assigned_to_id=obj_in.assigned_to_id,
            created_by_id=created_by_id,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def add_comment(
        self, db: AsyncSession, case_id: uuid.UUID, author_id: uuid.UUID, obj_in: CaseCommentCreate
    ) -> CaseComment:
        comment = CaseComment(case_id=case_id, author_id=author_id, content=obj_in.content)
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        return comment

    async def add_timeline_event(
        self,
        db: AsyncSession,
        case_id: uuid.UUID,
        event_type: TimelineEventType,
        description: str,
        actor_id: Optional[uuid.UUID] = None,
    ) -> CaseTimeline:
        event = CaseTimeline(
            case_id=case_id, event_type=event_type, description=description, actor_id=actor_id
        )
        db.add(event)
        await db.commit()
        await db.refresh(event)
        return event

case_repo = CRUDCase(Case)
