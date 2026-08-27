from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class QueryUnderstanding(BaseModel):
    """Parsed query intent, language, and parameters."""
    intent: str  # financial_health | affordability | repayment | loan_scenario | anomaly_explanation | digital_twin | what_if_simulation
    detected_language: str = "en"  # en | hi | hinglish
    extracted_params: Dict[str, Any] = Field(default_factory=dict)
    required_data_sources: List[str] = Field(default_factory=list)


class FinancialIntelligenceRequest(BaseModel):
    """Request structure for Financial Intelligence service."""
    request_id: str
    user_id: Optional[int] = None
    query: str
    task: Optional[str] = None  # Auto-detected if not specified
    language: str = "auto"  # auto | en | hi | hinglish
    context: Dict[str, Any] = Field(default_factory=dict)


class FinancialIntelligenceResponse(BaseModel):
    """Structured response for Financial Intelligence service."""
    request_id: str
    task: str
    language: str
    query_understanding: QueryUnderstanding
    deterministic_results: Dict[str, Any] = Field(default_factory=dict)
    explanation: str
    evidence: List[str] = Field(default_factory=list)
    recommendation: str = "advise"  # approve | review | reject | escalate | advise
    confidence: float = Field(ge=0.0, le=1.0, default=0.95)
    digital_twin_state: Optional[Dict[str, Any]] = None
    what_if_result: Optional[Dict[str, Any]] = None
