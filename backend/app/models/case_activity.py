import enum
import uuid
from typing import Optional
from sqlalchemy import Enum as SAEnum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, UUIDMixin, TimestampMixin


class TimelineEventType(str, enum.Enum):
    CASE_CREATED = "CASE_CREATED"
    CASE_UPDATED = "CASE_UPDATED"
    STATUS_CHANGED = "STATUS_CHANGED"
    SEVERITY_CHANGED = "SEVERITY_CHANGED"
    ALERT_LINKED = "ALERT_LINKED"
    COMMENT_ADDED = "COMMENT_ADDED"
    ASSIGNEE_CHANGED = "ASSIGNEE_CHANGED"
    NOTE_ADDED = "NOTE_ADDED"


class CaseComment(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "case_comments"

    case_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False, index=True
    )
    author_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Relationships
    case = relationship("Case", back_populates="comments", lazy="select")
    author = relationship("User", lazy="selectin")


class CaseTimeline(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "case_timeline"

    case_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False, index=True
    )
    event_type: Mapped[TimelineEventType] = mapped_column(
        SAEnum(TimelineEventType, name="timelineeventtype"), nullable=False
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    actor_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    case = relationship("Case", back_populates="timeline", lazy="select")
    actor = relationship("User", lazy="selectin")
