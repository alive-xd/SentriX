import uuid
from typing import List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models.case import Case, CaseStatus, CaseSeverity
from app.models.case_activity import CaseComment, TimelineEventType
from app.models.user import User
from app.schemas.case import CaseCreate, CaseUpdate
from app.schemas.alert import AlertPromote, AlertUpdate
from app.schemas.case_activity import CaseCommentCreate
from app.repositories.case_repository import case_repo
from app.services.alert_service import alert_service


class CaseService:
    async def get_cases(
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
        return await case_repo.get_multi_with_filters(
            db, skip=skip, limit=limit, status=status, severity=severity, 
            assigned_to_id=assigned_to_id, search=search, 
            sort_by=sort_by, sort_desc=sort_desc
        )

    async def get_case(self, db: AsyncSession, case_id: uuid.UUID) -> Case:
        case = await case_repo.get(db, id=case_id)
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        return case

    async def create_case(self, db: AsyncSession, case_in: CaseCreate, current_user: User) -> Case:
        case = await case_repo.create_with_author(db, obj_in=case_in, created_by_id=current_user.id)
        await case_repo.add_timeline_event(
            db, case_id=case.id, event_type=TimelineEventType.CASE_CREATED, 
            description="Case created", actor_id=current_user.id
        )
        return case

    async def update_case(self, db: AsyncSession, case_id: uuid.UUID, case_in: CaseUpdate, current_user: User) -> Case:
        case = await self.get_case(db, case_id)
        
        # Determine what changed for timeline
        changes = []
        if case_in.status and case_in.status != case.status:
            changes.append(f"Status changed to {case_in.status.value}")
        if case_in.severity and case_in.severity != case.severity:
            changes.append(f"Severity changed to {case_in.severity.value}")
            
        updated_case = await case_repo.update(db, db_obj=case, obj_in=case_in)
        
        for change in changes:
            await case_repo.add_timeline_event(
                db, case_id=updated_case.id, event_type=TimelineEventType.CASE_UPDATED,
                description=change, actor_id=current_user.id
            )
            
        return updated_case

    async def delete_case(self, db: AsyncSession, case_id: uuid.UUID) -> None:
        case = await self.get_case(db, case_id)
        await case_repo.soft_delete(db, id=case.id)

    async def add_comment(self, db: AsyncSession, case_id: uuid.UUID, obj_in: CaseCommentCreate, current_user: User) -> CaseComment:
        case = await self.get_case(db, case_id)
        comment = await case_repo.add_comment(db, case_id=case.id, author_id=current_user.id, obj_in=obj_in)
        
        await case_repo.add_timeline_event(
            db, case_id=case.id, event_type=TimelineEventType.COMMENT_ADDED,
            description="Comment added", actor_id=current_user.id
        )
        return comment

    async def promote_alert(self, db: AsyncSession, alert_id: uuid.UUID, promote_in: AlertPromote, current_user: User) -> Case:
        alert = await alert_service.get_alert(db, alert_id)
        
        if promote_in.case_id:
            case = await self.get_case(db, promote_in.case_id)
        else:
            title = promote_in.case_title or f"Case from Alert: {alert.title}"
            case_create = CaseCreate(
                title=title,
                description=alert.description,
                severity=CaseSeverity(alert.severity.value),
                source=alert.source,
                tags=alert.tags or [],
            )
            case = await self.create_case(db, case_in=case_create, current_user=current_user)
            
        # Link alert
        await alert_service.update_alert(db, alert_id, alert_in=AlertUpdate(case_id=case.id))
        
        await case_repo.add_timeline_event(
            db, case_id=case.id, event_type=TimelineEventType.ALERT_LINKED,
            description=f"Alert {alert.title} linked to case", actor_id=current_user.id
        )
        
        return case


case_service = CaseService()
