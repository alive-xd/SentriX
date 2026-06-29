import enum
from sqlalchemy import String, Text, Enum as SAEnum, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional, List
from sqlalchemy import String, Text, Enum as SAEnum, Boolean, Integer, Float, ARRAY, DateTime
from app.db.base_class import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin


class PlaybookStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    DRAFT = "DRAFT"
    ARCHIVED = "ARCHIVED"


class Playbook(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "playbooks"

    name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    trigger_type: Mapped[str] = mapped_column(String(100), nullable=False) # e.g. "ON_ALERT_CREATED"
    
    status: Mapped[PlaybookStatus] = mapped_column(
        SAEnum(PlaybookStatus, name="playbookstatus"), nullable=False, default=PlaybookStatus.DRAFT
    )
    
    steps: Mapped[Optional[List[dict]]] = mapped_column(JSONB, nullable=True) # Definition of the DAG or workflow steps
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    author: Mapped[str] = mapped_column(String(255), default="System", server_default="System")
    runs: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    success_rate: Mapped[float] = mapped_column(Float, default=0.0, server_default="0.0")
    avg_duration_s: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    last_run: Mapped[Optional[str]] = mapped_column(DateTime, nullable=True)
    tags: Mapped[List[str]] = mapped_column(ARRAY(String), default=[], server_default='{}')
    integrations: Mapped[List[str]] = mapped_column(ARRAY(String), default=[], server_default='{}')

class ExecStatus(str, enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    RUNNING = "RUNNING"
    SKIPPED = "SKIPPED"

class PlaybookExecution(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "playbook_executions"
    
    playbook_name: Mapped[str] = mapped_column(String(255), nullable=False)
    trigger: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[ExecStatus] = mapped_column(SAEnum(ExecStatus, name="execstatus"), nullable=False)
    started_at: Mapped[str] = mapped_column(DateTime, nullable=False)
    duration_s: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    steps_completed: Mapped[int] = mapped_column(Integer, default=0)
    steps_total: Mapped[int] = mapped_column(Integer, default=0)
    analyst: Mapped[str] = mapped_column(String(255), nullable=False)

