from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from app.models.playbook import PlaybookStatus, ExecStatus

# --- Playbook Execution ---
class PlaybookExecutionBase(BaseModel):
    playbook_name: str
    trigger: str
    status: ExecStatus
    started_at: datetime
    duration_s: Optional[int] = None
    steps_completed: int = 0
    steps_total: int = 0
    analyst: str

class PlaybookExecutionRead(PlaybookExecutionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Playbook ---
class PlaybookBase(BaseModel):
    name: str
    description: Optional[str] = None
    trigger_type: str
    status: PlaybookStatus = PlaybookStatus.DRAFT
    steps: Optional[List[Dict[str, Any]]] = None
    is_active: bool = False
    
    author: str = "System"
    runs: int = 0
    success_rate: float = 0.0
    avg_duration_s: int = 0
    last_run: Optional[str] = None
    tags: List[str] = []
    integrations: List[str] = []

class PlaybookCreate(PlaybookBase):
    pass

class PlaybookUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    trigger_type: Optional[str] = None
    status: Optional[PlaybookStatus] = None
    steps: Optional[List[Dict[str, Any]]] = None
    is_active: Optional[bool] = None
    tags: Optional[List[str]] = None
    integrations: Optional[List[str]] = None

class PlaybookRead(PlaybookBase):
    id: UUID
    # trigger alias for frontend mapping
    trigger: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
