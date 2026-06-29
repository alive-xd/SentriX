import enum
import uuid
from typing import Optional, List
from sqlalchemy import (
    Enum as SAEnum, ForeignKey, Integer, String, Text, ARRAY
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin


class CaseSeverity(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class CaseStatus(str, enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"
    FALSE_POSITIVE = "FALSE_POSITIVE"


class Case(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "cases"

    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    severity: Mapped[CaseSeverity] = mapped_column(
        SAEnum(CaseSeverity, name="caseseverity"), nullable=False, default=CaseSeverity.MEDIUM
    )
    status: Mapped[CaseStatus] = mapped_column(
        SAEnum(CaseStatus, name="casestatus"), nullable=False, default=CaseStatus.OPEN
    )
    priority: Mapped[int] = mapped_column(Integer, default=3)
    source: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    assigned_to_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )
    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )
    tags: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True, default=[])
    mitre_tactics: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True, default=[])
    extra_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Relationships
    assigned_to = relationship("User", foreign_keys=[assigned_to_id], lazy="selectin")
    created_by = relationship("User", foreign_keys=[created_by_id], lazy="selectin")
    alerts = relationship("Alert", back_populates="case", lazy="selectin", cascade="all, delete-orphan")
    comments = relationship("CaseComment", back_populates="case", lazy="selectin", cascade="all, delete-orphan")
    timeline = relationship("CaseTimeline", back_populates="case", order_by="CaseTimeline.created_at", lazy="selectin", cascade="all, delete-orphan")
    investigations = relationship("Investigation", back_populates="case", lazy="selectin", cascade="all, delete-orphan")
