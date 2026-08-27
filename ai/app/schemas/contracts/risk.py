from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RiskAssessmentDTO(BaseModel):
    """Canonical contract DTO for Credit Risk Assessment."""
    entity_id: str = Field(description="Unique entity or customer ID")
    risk_score: int = Field(ge=300, le=850, description="Credit risk score")
    probability_of_default: float = Field(ge=0.0, le=1.0, description="Calibrated default probability")
    risk_level: str = Field(description="Risk tier e.g. low, medium, high, critical")
    confidence: float = Field(ge=0.0, le=1.0, description="Model prediction confidence")
    attributions: List[Dict[str, Any]] = Field(default_factory=list, description="Feature attribution payloads")
    evidence: Dict[str, Any] = Field(default_factory=dict, description="Auditable prediction evidence")
    recommendation: str = Field(description="Suggested decision e.g. approve, review, reject")
    model_version: str = Field(default="1.0.0", description="Model version identifier")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="ISO timestamp")
