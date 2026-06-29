from uuid import UUID
from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field
from app.models.investigation import InvestigationStatus


class InvestigationBase(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    description: Optional[str] = None
    status: InvestigationStatus = InvestigationStatus.PENDING
    findings: Optional[dict[str, Any]] = None
    case_id: UUID
    assigned_to_id: Optional[UUID] = None


class InvestigationCreate(InvestigationBase):
    pass


class InvestigationUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=255)
    description: Optional[str] = None
    status: Optional[InvestigationStatus] = None
    findings: Optional[dict[str, Any]] = None
    assigned_to_id: Optional[UUID] = None


class InvestigationRead(InvestigationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
