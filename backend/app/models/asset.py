import enum
import uuid
from typing import Optional, List
from sqlalchemy import (
    Enum as SAEnum, Float, ForeignKey, String, Text, ARRAY
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base_class import Base, UUIDMixin, TimestampMixin, SoftDeleteMixin


class AssetType(str, enum.Enum):
    ENDPOINT = "ENDPOINT"
    SERVER = "SERVER"
    NETWORK_DEVICE = "NETWORK_DEVICE"
    CLOUD_RESOURCE = "CLOUD_RESOURCE"
    CONTAINER = "CONTAINER"
    IOT = "IOT"


class AssetCriticality(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class AssetStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DECOMMISSIONED = "DECOMMISSIONED"
    UNKNOWN = "UNKNOWN"


class VulnerabilitySeverity(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFORMATIONAL = "INFORMATIONAL"


class VulnerabilityStatus(str, enum.Enum):
    OPEN = "OPEN"
    REMEDIATED = "REMEDIATED"
    ACCEPTED = "ACCEPTED"
    IN_PROGRESS = "IN_PROGRESS"


class Asset(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "assets"

    hostname: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True, index=True)
    mac_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    os_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    os_version: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    asset_type: Mapped[AssetType] = mapped_column(
        SAEnum(AssetType, name="assettype"), nullable=False, default=AssetType.ENDPOINT
    )
    criticality: Mapped[AssetCriticality] = mapped_column(
        SAEnum(AssetCriticality, name="assetcriticality"), nullable=False, default=AssetCriticality.MEDIUM
    )
    status: Mapped[AssetStatus] = mapped_column(
        SAEnum(AssetStatus, name="assetstatus"), nullable=False, default=AssetStatus.ACTIVE
    )
    owner: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    tags: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True, default=[])
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    extra_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Relationships
    vulnerabilities = relationship("AssetVulnerability", back_populates="asset", lazy="selectin", cascade="all, delete-orphan")


class AssetVulnerability(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "asset_vulnerabilities"

    asset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    cve_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    title: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    severity: Mapped[VulnerabilitySeverity] = mapped_column(
        SAEnum(VulnerabilitySeverity, name="vulnerabilityseverity"), nullable=False
    )
    status: Mapped[VulnerabilityStatus] = mapped_column(
        SAEnum(VulnerabilityStatus, name="vulnerabilitystatus"), nullable=False, default=VulnerabilityStatus.OPEN
    )
    cvss_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    remediation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    asset = relationship("Asset", back_populates="vulnerabilities", lazy="select")
