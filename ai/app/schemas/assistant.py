from decimal import Decimal
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AssistantQueryRequest(BaseModel):
    user_id: int
    target_user_id: Optional[int] = None
    organization_id: str
    role: str = "USER"  # "USER" | "BANKER"
    language: Optional[str] = None  # "en" | "hi" | "hinglish"
    message: str



class FactItem(BaseModel):
    label: str
    value: str  # Preserved exact format e.g. "₹80,000.00"
    source: str = "Member 1 Authoritative Financial API"


class CalculationItem(BaseModel):
    label: str
    value: str  # Preserved exact format e.g. "₹11,249.00"
    formula: str = "Deterministic Financial Engine"


class RiskSignalItem(BaseModel):
    model_name: str
    score: float
    status: str = "EXPERIMENTAL"
    reason_codes: List[str] = Field(default_factory=list)


class CitationItem(BaseModel):
    document_id: str
    snippet: str
    relevance_score: float


class AssistantQueryResponse(BaseModel):
    request_id: str
    answer: str
    language: str
    intent: str
    facts: List[FactItem] = Field(default_factory=list)
    calculations: List[CalculationItem] = Field(default_factory=list)
    risk_signals: List[RiskSignalItem] = Field(default_factory=list)
    sources: List[CitationItem] = Field(default_factory=list)
    confidence: float = 0.95
    requires_human_review: bool = False
    model_metadata: Dict[str, Any] = Field(default_factory=dict)
