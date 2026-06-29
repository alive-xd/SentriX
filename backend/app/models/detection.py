import enum
import uuid
from typing import Optional, List
from sqlalchemy import (
    Boolean, Enum as SAEnum, ForeignKey, Integer, String, Text, ARRAY
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, UUIDMixin, TimestampMixin


class RuleType(str, enum.Enum):
    SIGMA = "SIGMA"
    YARA = "YARA"
    CUSTOM = "CUSTOM"
    KQL = "KQL"
    SPL = "SPL"


class RuleSeverity(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class RuleStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    TESTING = "TESTING"
    DEPRECATED = "DEPRECATED"


class RuleTestStatus(str, enum.Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    ERROR = "ERROR"


class DetectionRule(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "detection_rules"

    name: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    rule_type: Mapped[RuleType] = mapped_column(
        SAEnum(RuleType, name="ruletype"), nullable=False, default=RuleType.SIGMA
    )
    severity: Mapped[RuleSeverity] = mapped_column(
        SAEnum(RuleSeverity, name="ruleseverity"), nullable=False, default=RuleSeverity.MEDIUM
    )
    status: Mapped[RuleStatus] = mapped_column(
        SAEnum(RuleStatus, name="rulestatus"), nullable=False, default=RuleStatus.TESTING
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)  # Raw SIGMA/YARA/Custom rule body
    mitre_tactic: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mitre_technique: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    tags: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), nullable=True, default=[])
    hit_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    false_positive_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )
    last_modified_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    created_by = relationship("User", foreign_keys=[created_by_id], lazy="selectin")
    last_modified_by = relationship("User", foreign_keys=[last_modified_by_id], lazy="selectin")
    test_runs = relationship("RuleTest", back_populates="rule", order_by="RuleTest.created_at.desc()", lazy="select")


class RuleTest(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "rule_tests"

    rule_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("detection_rules.id", ondelete="CASCADE"), nullable=False, index=True
    )
    ran_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[RuleTestStatus] = mapped_column(
        SAEnum(RuleTestStatus, name="ruleteststatus"), nullable=False
    )
    result_output: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    rule = relationship("DetectionRule", back_populates="test_runs", lazy="select")
    ran_by = relationship("User", lazy="selectin")
