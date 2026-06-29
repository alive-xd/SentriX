from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.asset import (
    AssetType, AssetCriticality, AssetStatus,
    VulnerabilitySeverity, VulnerabilityStatus
)


# --- Asset Schemas ---

class AssetBase(BaseModel):
    hostname: str = Field(min_length=1, max_length=255)
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    os_type: Optional[str] = None
    os_version: Optional[str] = None
    asset_type: AssetType = AssetType.ENDPOINT
    criticality: AssetCriticality = AssetCriticality.MEDIUM
    status: AssetStatus = AssetStatus.ACTIVE
    owner: Optional[str] = None
    location: Optional[str] = None
    risk_score: float = Field(default=0.0, ge=0.0, le=100.0)
    tags: Optional[List[str]] = []
    description: Optional[str] = None


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    hostname: Optional[str] = Field(default=None, min_length=1, max_length=255)
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    os_type: Optional[str] = None
    os_version: Optional[str] = None
    asset_type: Optional[AssetType] = None
    criticality: Optional[AssetCriticality] = None
    status: Optional[AssetStatus] = None
    owner: Optional[str] = None
    location: Optional[str] = None
    risk_score: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    tags: Optional[List[str]] = None
    description: Optional[str] = None


class AssetRead(AssetBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AssetStats(BaseModel):
    total: int
    active: int
    critical: int
    high_risk_count: int  # risk_score > 70


# --- Vulnerability Schemas ---

class VulnerabilityCreate(BaseModel):
    cve_id: str = Field(min_length=3, max_length=50)
    title: Optional[str] = None
    severity: VulnerabilitySeverity
    status: VulnerabilityStatus = VulnerabilityStatus.OPEN
    cvss_score: Optional[float] = Field(default=None, ge=0.0, le=10.0)
    description: Optional[str] = None
    remediation: Optional[str] = None


class VulnerabilityUpdate(BaseModel):
    title: Optional[str] = None
    severity: Optional[VulnerabilitySeverity] = None
    status: Optional[VulnerabilityStatus] = None
    cvss_score: Optional[float] = Field(default=None, ge=0.0, le=10.0)
    description: Optional[str] = None
    remediation: Optional[str] = None


class VulnerabilityRead(VulnerabilityCreate):
    id: UUID
    asset_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
