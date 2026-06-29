from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.case import CaseSeverity, CaseStatus
from app.schemas.user import UserRead


class CaseBase(BaseModel):
    title: str = Field(min_length=3, max_length=500)
    description: Optional[str] = None
    severity: CaseSeverity = CaseSeverity.MEDIUM
    status: CaseStatus = CaseStatus.OPEN
    priority: int = Field(default=3, ge=1, le=5)
    source: Optional[str] = None
    tags: Optional[List[str]] = []
    mitre_tactics: Optional[List[str]] = []
    assigned_to_id: Optional[UUID] = None


class CaseCreate(CaseBase):
    pass


class CaseUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=500)
    description: Optional[str] = None
    severity: Optional[CaseSeverity] = None
    status: Optional[CaseStatus] = None
    priority: Optional[int] = Field(default=None, ge=1, le=5)
    source: Optional[str] = None
    tags: Optional[List[str]] = None
    mitre_tactics: Optional[List[str]] = None
    assigned_to_id: Optional[UUID] = None


class CaseRead(CaseBase):
    id: UUID
    created_by_id: Optional[UUID] = None
    assigned_to: Optional[UserRead] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CaseReadWithDetails(CaseRead):
    alert_count: int = 0
    comment_count: int = 0
