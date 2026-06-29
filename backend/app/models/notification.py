import enum
import uuid
from sqlalchemy import String, Text, ForeignKey, Enum as SAEnum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from typing import Optional
from app.db.base_class import Base, UUIDMixin, TimestampMixin


class NotificationType(str, enum.Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ALERT = "ALERT"
    SYSTEM = "SYSTEM"


class Notification(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "notifications"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    
    type: Mapped[NotificationType] = mapped_column(
        SAEnum(NotificationType, name="notificationtype"), nullable=False, default=NotificationType.INFO
    )
    
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    link: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True) # Direct link to related entity
    extra_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Relationships
    user = relationship("User", lazy="selectin")
