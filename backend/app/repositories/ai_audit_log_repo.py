from typing import List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
import sqlalchemy

from app.models.ai_audit_log import AIAuditLog
from app.repositories.base import CRUDBase

class CRUDAIAuditLog(CRUDBase[AIAuditLog, AIAuditLog, AIAuditLog]): # Simplified typing since we don't have separate Pydantic schemas yet
    async def get_logs_by_target(
        self, db: AsyncSession, *, target_type: str, target_id: str, skip: int = 0, limit: int = 100
    ) -> Tuple[List[AIAuditLog], int]:
        query = select(AIAuditLog).filter(
            AIAuditLog.target_entity_type == target_type,
            AIAuditLog.target_entity_id == target_id
        )
        total_res = await db.execute(select(sqlalchemy.func.count()).select_from(query.subquery()))
        total = total_res.scalar_one()

        query = query.order_by(desc(AIAuditLog.created_at)).offset(skip).limit(limit)
        result = await db.execute(query)
        items = result.scalars().all()
        return list(items), total

ai_audit_log_repo = CRUDAIAuditLog(AIAuditLog)
