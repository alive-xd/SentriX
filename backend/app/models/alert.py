import enum
import uuid
from typing import Optional, List
from sqlalchemy import (
    Enum as SAEnum, ForeignKey, String, Text, ARRAY
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin


class AlertSeverity(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class AlertStatus(str, enum.Enum):
    NEW = "NEW"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    FALSE_POSITIVE = "FALSE_POSITIVE"


class Alert(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "alerts"

    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    severity: Mapped[AlertSeverity] = mapped_column(
        SAEnum(AlertSeverity, name="alertseverity"), nullable=False, default=AlertSeverity.MEDIUM
    )
    status: Mapped[AlertStatus] = mapped_column(
        SAEnum(AlertStatus, name="alertstatus"), nullable=False, default=AlertStatus.NEW
    )
    rule_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    source: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    source_ip: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    dest_ip: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    mitre_tactic: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mitre_technique: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    raw_log: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tags: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True, default=[])
    extra_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    case_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cases.id", ondelete="SET NULL"), nullable=True, index=True
    )
    assigned_to_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    case = relationship("Case", back_populates="alerts", lazy="select")
    assigned_to = relationship("User", foreign_keys=[assigned_to_id], lazy="selectin")
