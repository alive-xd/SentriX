import uuid
from typing import List, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models.alert import Alert, AlertStatus, AlertSeverity
from app.schemas.alert import AlertCreate, AlertUpdate
from app.repositories.alert_repository import alert_repo


class AlertService:
    async def get_alerts(
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
        return await alert_repo.get_multi_with_filters(
            db, skip=skip, limit=limit, status=status, severity=severity, 
            case_id=case_id, assigned_to_id=assigned_to_id, 
            search=search, sort_by=sort_by, sort_desc=sort_desc
        )

    async def get_alert(self, db: AsyncSession, alert_id: uuid.UUID) -> Alert:
        alert = await alert_repo.get(db, id=alert_id)
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        return alert

    async def create_alert(self, db: AsyncSession, alert_in: AlertCreate) -> Alert:
        return await alert_repo.create(db, obj_in=alert_in)

    async def update_alert(self, db: AsyncSession, alert_id: uuid.UUID, alert_in: AlertUpdate) -> Alert:
        alert = await self.get_alert(db, alert_id)
        return await alert_repo.update(db, db_obj=alert, obj_in=alert_in)

    async def delete_alert(self, db: AsyncSession, alert_id: uuid.UUID) -> None:
        alert = await self.get_alert(db, alert_id)
        await alert_repo.soft_delete(db, id=alert.id)

    async def assign_alert(self, db: AsyncSession, alert_id: uuid.UUID, user_id: uuid.UUID) -> Alert:
        alert = await self.get_alert(db, alert_id)
        return await alert_repo.update(db, db_obj=alert, obj_in=AlertUpdate(assigned_to_id=user_id))

    async def update_status(self, db: AsyncSession, alert_id: uuid.UUID, status: AlertStatus) -> Alert:
        alert = await self.get_alert(db, alert_id)
        return await alert_repo.update(db, db_obj=alert, obj_in=AlertUpdate(status=status))


alert_service = AlertService()
