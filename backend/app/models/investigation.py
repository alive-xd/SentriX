import enum
import uuid
from sqlalchemy import String, Text, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from typing import Optional
from app.db.base_class import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin


class InvestigationStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"


class Investigation(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "investigations"

    case_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False, index=True
    )
    assigned_to_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="SET NULL"), nullable=True, index=True
    )
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[InvestigationStatus] = mapped_column(
        SAEnum(InvestigationStatus, name="investigationstatus"), nullable=False, default=InvestigationStatus.PENDING
    )
    findings: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Relationships
    case = relationship("Case", back_populates="investigations", lazy="select")
    assigned_to = relationship("User", lazy="select")
