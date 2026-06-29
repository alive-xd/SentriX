from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class SavedHuntBase(BaseModel):
    name: str
    description: Optional[str] = None
    query: str
    category: str = "General"
    starred: bool = False
    last_run: Optional[str] = None

class SavedHuntCreate(SavedHuntBase):
    pass

class SavedHuntUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    query: Optional[str] = None
    category: Optional[str] = None
    starred: Optional[bool] = None
    last_run: Optional[str] = None

class SavedHuntInDBBase(SavedHuntBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SavedHunt(SavedHuntInDBBase):
    pass

class HuntResultBase(BaseModel):
    id: str
    timestamp: str
    host: str
    user: str
    event_id: str
    parent_process: str
    process_name: str
    command_line: str
    sha256: str
    risk_score: int
    mitre_technique: str
    detection_rule: str
