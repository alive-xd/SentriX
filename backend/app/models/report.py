import enum
import uuid
from sqlalchemy import String, Text, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from typing import Optional
from app.db.base_class import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin


class ReportStatus(str, enum.Enum):
    PENDING = "PENDING"
    GENERATING = "GENERATING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Report(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "reports"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    report_type: Mapped[str] = mapped_column(String(100), nullable=False) # e.g. "WEEKLY_SUMMARY", "EXECUTIVE_DASHBOARD"
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    status: Mapped[ReportStatus] = mapped_column(
        SAEnum(ReportStatus, name="reportstatus"), nullable=False, default=ReportStatus.PENDING
    )
    
    config: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True) # Filters, parameters used for generation
    file_url: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True) # S3 or local path
    
    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="SET NULL"), nullable=True, index=True
    )
    
    # Relationships
    created_by = relationship("User", lazy="selectin")
