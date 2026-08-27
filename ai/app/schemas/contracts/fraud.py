from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FraudSignalDTO(BaseModel):
    """Canonical contract DTO for Fraud & Anomaly Signals."""
    entity_id: str = Field(description="Customer or account identifier")
    transaction_id: Optional[str] = Field(default=None, description="Optional transaction ID")
    fraud_type: str = Field(description="Category of fraud e.g. velocity_spike, account_takeover, transaction_anomaly")
    severity: str = Field(description="Severity e.g. info, warning, high, critical")
    score: int = Field(ge=0, le=100, description="Scaled fraud score 0-100")
    evidence: Dict[str, Any] = Field(default_factory=dict, description="Supporting evidence payload")
    status: str = Field(default="open", description="Signal status e.g. open, under_review, resolved")
    model_version: str = Field(default="1.0.0", description="Model version identifier")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="ISO timestamp")


class FraudAssessmentDTO(BaseModel):
    """Canonical contract DTO for overall Fraud Assessment."""
    entity_id: str
    overall_fraud_score: float = Field(ge=0.0, le=1.0)
    signals: List[FraudSignalDTO] = Field(default_factory=list)
    requires_immediate_block: bool = Field(default=False)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
