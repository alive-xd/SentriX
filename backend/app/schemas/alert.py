from uuid import UUID
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, Field
from app.models.alert import AlertSeverity, AlertStatus


class AlertBase(BaseModel):
    title: str = Field(min_length=3, max_length=500)
    description: Optional[str] = None
    severity: AlertSeverity = AlertSeverity.MEDIUM
    status: AlertStatus = AlertStatus.NEW
    rule_id: Optional[str] = None
    source: Optional[str] = None
    source_ip: Optional[str] = None
    dest_ip: Optional[str] = None
    mitre_tactic: Optional[str] = None
    mitre_technique: Optional[str] = None
    raw_log: Optional[str] = None
    tags: Optional[List[str]] = []
    extra_data: Optional[dict[str, Any]] = None


class AlertCreate(AlertBase):
    pass


class AlertUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=500)
    description: Optional[str] = None
    severity: Optional[AlertSeverity] = None
    status: Optional[AlertStatus] = None
    rule_id: Optional[str] = None
    source_ip: Optional[str] = None
    dest_ip: Optional[str] = None
    mitre_tactic: Optional[str] = None
    mitre_technique: Optional[str] = None
    raw_log: Optional[str] = None
    tags: Optional[List[str]] = None
    extra_data: Optional[dict[str, Any]] = None
    case_id: Optional[UUID] = None
    assigned_to_id: Optional[UUID] = None


class AlertRead(AlertBase):
    id: UUID
    case_id: Optional[UUID] = None
    assigned_to_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# For promoting an alert to a new or existing case
class AlertPromote(BaseModel):
    case_id: Optional[UUID] = None   # link to existing case
    case_title: Optional[str] = None # create new case with this title
