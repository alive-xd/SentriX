from typing import List, Optional, Tuple
from sqlalchemy import select, func, and_, or_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.repositories.base import CRUDBase
from app.models.alert import Alert, AlertStatus, AlertSeverity
from app.schemas.alert import AlertCreate, AlertUpdate


class CRUDAlert(CRUDBase[Alert, AlertCreate, AlertUpdate]):
    async def get_multi_with_filters(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 50,
        status: Optional[AlertStatus] = None,
        severity: Optional[AlertSeverity] = None,
        case_id: Optional[uuid.UUID] = None,
        assigned_to_id: Optional[uuid.UUID] = None,
        search: Optional[str] = None,
        sort_by: str = "created_at",
        sort_desc: bool = True
    ) -> Tuple[List[Alert], int]:
        
        query = select(self.model)
        filters = []
        
        if status:
            filters.append(self.model.status == status)
        if severity:
            filters.append(self.model.severity == severity)
        if case_id:
            filters.append(self.model.case_id == case_id)
        if assigned_to_id:
            filters.append(self.model.assigned_to_id == assigned_to_id)
        if search:
            filters.append(
                or_(
                    self.model.title.ilike(f"%{search}%"),
                    self.model.description.ilike(f"%{search}%"),
                    self.model.source_ip.ilike(f"%{search}%"),
                )
            )
            
        if filters:
            query = query.where(and_(*filters))
            
        # Count total
        count_result = await db.execute(select(func.count()).select_from(query.subquery()))
        total = count_result.scalar_one()
        
        # Sorting
        sort_column = getattr(self.model, sort_by, self.model.created_at)
        if sort_desc:
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
            
        # Pagination
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all(), total

alert_repo = CRUDAlert(Alert)
