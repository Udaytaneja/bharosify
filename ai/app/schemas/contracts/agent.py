from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AgentIntelligenceRequestDTO(BaseModel):
    """Canonical contract DTO for Agent action governance evaluation request."""
    agent_id: str = Field(description="Agent identity string")
    organization_id: Optional[str] = Field(default=None, description="Multi-tenant organization boundary")
    user_id: Optional[str] = Field(default=None, description="Requesting user ID")
    action: str = Field(description="Action requested e.g. execute, transfer, delete")
    resource: str = Field(description="Target resource identifier")
    tool_name: Optional[str] = Field(default=None, description="Tool invoked")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Action payload parameters")
    context: Dict[str, Any] = Field(default_factory=dict, description="Execution environment context")


class AgentIntelligenceResponseDTO(BaseModel):
    """Canonical contract DTO for Agent governance decision response."""
    agent_id: str
    action: str
    resource: str
    decision: str = Field(description="Governed decision: ALLOW | HOLD | BLOCK | HUMAN_REVIEW")
    reason: str = Field(description="Reason code for auditability")
    risk_level: str = Field(description="Risk classification: low | medium | high | critical")
    risk_score: int = Field(ge=0, le=100)
    trust_score: int = Field(ge=0, le=1000)
    audit_explanation: str = Field(description="Human-readable auditable explanation")
    evidence: List[str] = Field(default_factory=list)
    violations: List[str] = Field(default_factory=list)
    anomalies: List[str] = Field(default_factory=list)
    requires_human_review: bool = Field(default=False)
    model_version: str = Field(default="1.0.0")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
