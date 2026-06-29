import uuid
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from typing import Optional
from app.db.base_class import Base, UUIDMixin, TimestampMixin


class AuditLog(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "audit_logs"

    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # e.g. "CREATE", "UPDATE", "DELETE", "LOGIN"
    entity_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True) # e.g. "Case", "Alert"
    entity_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    
    changes: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True) # Dictionary of old/new values
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="SET NULL"), nullable=True, index=True
    )

    # Relationships
    user = relationship("User", lazy="selectin")
