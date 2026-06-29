import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, JSON, Text
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

class AIAuditLog(Base):
    __tablename__ = "ai_audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_name = Column(String, index=True, nullable=False)
    target_entity_type = Column(String, index=True, nullable=False) # e.g., "Alert", "Case", "Malware"
    target_entity_id = Column(String, index=True, nullable=False)
    
    # Execution metrics
    prompt_tokens = Column(Float, nullable=True)
    completion_tokens = Column(Float, nullable=True)
    confidence_score = Column(Float, nullable=True)
    
    # Raw data for audit
    raw_request = Column(JSON, nullable=True)
    raw_response = Column(JSON, nullable=True)
    reasoning = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
