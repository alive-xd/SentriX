import enum
from sqlalchemy import String, Text, Enum as SAEnum, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional
from app.db.base_class import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin


class IntegrationStatus(str, enum.Enum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    ERROR = "ERROR"


class Integration(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "integrations"

    name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    provider: Mapped[str] = mapped_column(String(100), nullable=False) # e.g. "CROWDSTRIKE", "SPLUNK"
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    status: Mapped[IntegrationStatus] = mapped_column(
        SAEnum(IntegrationStatus, name="integrationstatus"), nullable=False, default=IntegrationStatus.DISCONNECTED
    )
    
    config: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True) # API Keys, URLs, etc.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
