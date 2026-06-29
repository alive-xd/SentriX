from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.threat_intel import (
    IndicatorType, IndicatorSeverity,
    ThreatActorSophistication, FeedType
)


# --- Threat Indicator ---

class ThreatIndicatorBase(BaseModel):
    type: IndicatorType
    value: str = Field(min_length=1, max_length=2048)
    severity: IndicatorSeverity = IndicatorSeverity.MEDIUM
    confidence: int = Field(default=50, ge=0, le=100)
    source: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True
    tags: Optional[List[str]] = []
    mitre_techniques: Optional[List[str]] = []
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None


class ThreatIndicatorCreate(ThreatIndicatorBase):
    pass


class ThreatIndicatorUpdate(BaseModel):
    severity: Optional[IndicatorSeverity] = None
    confidence: Optional[int] = Field(default=None, ge=0, le=100)
    source: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    tags: Optional[List[str]] = None
    mitre_techniques: Optional[List[str]] = None
    last_seen: Optional[str] = None


class ThreatIndicatorRead(ThreatIndicatorBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IndicatorLookup(BaseModel):
    values: List[str] = Field(min_length=1, max_length=100)


# --- Threat Actor ---

class ThreatActorBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    aliases: Optional[List[str]] = []
    description: Optional[str] = None
    motivation: Optional[str] = None
    sophistication: Optional[ThreatActorSophistication] = None
    target_sectors: Optional[List[str]] = []
    ttps: Optional[List[str]] = []
    is_active: bool = True


class ThreatActorCreate(ThreatActorBase):
    pass


class ThreatActorUpdate(BaseModel):
    aliases: Optional[List[str]] = None
    description: Optional[str] = None
    motivation: Optional[str] = None
    sophistication: Optional[ThreatActorSophistication] = None
    target_sectors: Optional[List[str]] = None
    ttps: Optional[List[str]] = None
    is_active: Optional[bool] = None


class ThreatActorRead(ThreatActorBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Threat Feed ---

class ThreatFeedBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    url: Optional[str] = None
    feed_type: FeedType = FeedType.MANUAL
    is_active: bool = True


class ThreatFeedCreate(ThreatFeedBase):
    pass


class ThreatFeedUpdate(BaseModel):
    description: Optional[str] = None
    url: Optional[str] = None
    feed_type: Optional[FeedType] = None
    is_active: Optional[bool] = None


class ThreatFeedRead(ThreatFeedBase):
    id: UUID
    indicator_count: int
    last_fetched: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
