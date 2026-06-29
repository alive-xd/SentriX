from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.case_activity import TimelineEventType
from app.schemas.user import UserRead


class CaseCommentCreate(BaseModel):
    content: str


class CaseCommentRead(BaseModel):
    id: UUID
    case_id: UUID
    author_id: Optional[UUID] = None
    content: str
    author: Optional[UserRead] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CaseTimelineRead(BaseModel):
    id: UUID
    case_id: UUID
    event_type: TimelineEventType
    description: str
    actor_id: Optional[UUID] = None
    actor: Optional[UserRead] = None
    created_at: datetime

    class Config:
        from_attributes = True
