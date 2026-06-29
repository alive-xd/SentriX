from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.detection import RuleType, RuleSeverity, RuleStatus, RuleTestStatus
from app.schemas.user import UserRead


class DetectionRuleBase(BaseModel):
    name: str = Field(min_length=3, max_length=500)
    description: Optional[str] = None
    rule_type: RuleType = RuleType.SIGMA
    severity: RuleSeverity = RuleSeverity.MEDIUM
    status: RuleStatus = RuleStatus.TESTING
    content: str = Field(min_length=1)
    mitre_tactic: Optional[str] = None
    mitre_technique: Optional[str] = None
    tags: Optional[List[str]] = []


class DetectionRuleCreate(DetectionRuleBase):
    pass


class DetectionRuleUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=500)
    description: Optional[str] = None
    rule_type: Optional[RuleType] = None
    severity: Optional[RuleSeverity] = None
    status: Optional[RuleStatus] = None
    content: Optional[str] = None
    mitre_tactic: Optional[str] = None
    mitre_technique: Optional[str] = None
    tags: Optional[List[str]] = None


class DetectionRuleRead(DetectionRuleBase):
    id: UUID
    hit_count: int
    false_positive_count: int
    is_enabled: bool
    created_by_id: Optional[UUID] = None
    last_modified_by_id: Optional[UUID] = None
    created_by: Optional[UserRead] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DetectionRuleStats(BaseModel):
    total: int
    active: int
    testing: int
    inactive: int
    total_hits: int


class RuleTestCreate(BaseModel):
    result_output: Optional[str] = None
    status: RuleTestStatus


class RuleTestRead(BaseModel):
    id: UUID
    rule_id: UUID
    status: RuleTestStatus
    result_output: Optional[str] = None
    ran_by: Optional[UserRead] = None
    created_at: datetime

    class Config:
        from_attributes = True
