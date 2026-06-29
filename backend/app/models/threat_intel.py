import enum
from typing import Optional, List
from sqlalchemy import (
    Boolean, Enum as SAEnum, Integer, String, Text, ARRAY
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin


class IndicatorType(str, enum.Enum):
    IP = "IP"
    DOMAIN = "DOMAIN"
    URL = "URL"
    FILE_HASH_MD5 = "FILE_HASH_MD5"
    FILE_HASH_SHA1 = "FILE_HASH_SHA1"
    FILE_HASH_SHA256 = "FILE_HASH_SHA256"
    EMAIL = "EMAIL"
    MUTEX = "MUTEX"
    REGISTRY_KEY = "REGISTRY_KEY"


class IndicatorSeverity(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ThreatIndicator(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "threat_indicators"

    type: Mapped[IndicatorType] = mapped_column(
        SAEnum(IndicatorType, name="indicatortype"), nullable=False, index=True
    )
    value: Mapped[str] = mapped_column(String(2048), nullable=False, index=True)
    severity: Mapped[IndicatorSeverity] = mapped_column(
        SAEnum(IndicatorSeverity, name="indicatorseverity"), nullable=False, default=IndicatorSeverity.MEDIUM
    )
    confidence: Mapped[int] = mapped_column(Integer, default=50)  # 0-100
    source: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    tags: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True, default=[])
    mitre_techniques: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True, default=[])
    first_seen: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    last_seen: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    extra_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

class ThreatActorSophistication(str, enum.Enum):
    NONE = "NONE"
    MINIMAL = "MINIMAL"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    EXPERT = "EXPERT"
    INNOVATOR = "INNOVATOR"


class ThreatActor(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "threat_actors"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    aliases: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True, default=[])
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    motivation: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    sophistication: Mapped[Optional[ThreatActorSophistication]] = mapped_column(
        SAEnum(ThreatActorSophistication, name="threatactorsophistication"), nullable=True
    )
    target_sectors: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True, default=[])
    ttps: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True, default=[])
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    extra_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

class FeedType(str, enum.Enum):
    STIX = "STIX"
    CSV = "CSV"
    JSON = "JSON"
    TAXII = "TAXII"
    MANUAL = "MANUAL"


class ThreatFeed(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "threat_feeds"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True)
    feed_type: Mapped[FeedType] = mapped_column(
        SAEnum(FeedType, name="feedtype"), nullable=False, default=FeedType.MANUAL
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    indicator_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_fetched: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    extra_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
