from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from app.models.report import ReportStatus

class ReportBase(BaseModel):
    title: str
    report_type: str
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    file_url: Optional[str] = None

class ReportCreate(ReportBase):
    status: Optional[ReportStatus] = ReportStatus.PENDING

class ReportUpdate(BaseModel):
    title: Optional[str] = None
    report_type: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ReportStatus] = None
    config: Optional[Dict[str, Any]] = None
    file_url: Optional[str] = None

class ReportInDBBase(ReportBase):
    id: str
    status: ReportStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Report(ReportInDBBase):
    pass
