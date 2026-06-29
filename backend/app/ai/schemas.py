from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

class AgentResponse(BaseModel):
    conclusion: str = Field(..., description="The main conclusion or outcome of the analysis.")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score of the conclusion from 0.0 to 1.0.")
    reasoning: str = Field(..., description="Detailed explanation of how the conclusion was reached.")
    evidence_collected: List[str] = Field(default_factory=list, description="Key pieces of evidence supporting the conclusion.")
    alternative_hypotheses: List[str] = Field(default_factory=list, description="Other possible explanations that were considered.")
    recommendations: List[str] = Field(default_factory=list, description="Recommended next steps or remediation actions.")
    raw_data: Optional[Dict[str, Any]] = Field(default=None, description="Any raw data returned by tools.")
