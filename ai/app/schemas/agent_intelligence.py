from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AgentRegistrationRequest(BaseModel):
    """Request payload for registering an autonomous agent."""
    agent_id: str
    name: str
    owner_id: Optional[int] = 1
    organization_id: str = "org_default"
    agent_type: str = "financial_advisor"  # digital_twin | underwriting | financial_advisor | risk_assessor | system
    capabilities: List[str] = Field(default_factory=lambda: ["financial_analysis", "cash_flow_tracking"])
    permissions: List[str] = Field(default_factory=lambda: ["financial_profile:read", "transactions:read"])
    policies: List[str] = Field(default_factory=lambda: ["max_amount_50k", "rate_limit_30m", "no_bulk_export"])


class AgentProfileResponse(BaseModel):
    """Agent identity, trust, risk, and permission profile response."""
    id: str
    name: str
    owner_id: int
    organization_id: str
    agent_type: str
    status: str  # active | pending | suspended | revoked
    trust_score: int
    risk_score: int
    capabilities: List[str]
    permissions: List[str]
    policies: List[str]


class AgentActionEvaluationRequest(BaseModel):
    """Payload to evaluate an agent action through the 9-stage pipeline."""
    agent_id: str
    action: str
    resource: str
    tool_name: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)


class AgentActionEvaluationResponse(BaseModel):
    """Decision output from the 9-stage Agent Intelligence evaluation pipeline."""
    agent_id: str
    action: str
    resource: str
    decision: str  # ALLOW | HOLD | BLOCK | HUMAN_REVIEW
    reason: str
    risk_level: str  # low | medium | high | critical
    risk_score: int
    trust_score: int
    audit_explanation: str
    evidence: List[str] = Field(default_factory=list)
    violations: List[str] = Field(default_factory=list)
    anomalies: List[str] = Field(default_factory=list)
    timestamp: str
