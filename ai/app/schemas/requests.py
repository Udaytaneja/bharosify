from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TelemetryMetadata(BaseModel):
    """Observable metadata for every model execution call."""
    request_id: str
    task: str
    model_id: str
    provider: str
    fallback_triggered: bool = False
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0
    latency_ms: float = 0.0
    retries_count: int = 0
    pii_redacted: bool = False
    prompt_shield_passed: bool = True
    decision_guard_passed: bool = True
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AIExecutionRequest(BaseModel):
    """Unified internal execution request payload."""
    request_id: str
    user_id: Optional[int] = None
    role: str = "user"  # user | banker
    task: str  # chat | scenario | risk_analysis | underwriting
    input: str
    language: str = "en"  # en | hi
    context: Dict[str, Any] = Field(default_factory=dict)
    temperature: float = 0.2
    max_tokens: int = 2048


class AIExecutionResponse(BaseModel):
    """Unified execution response matching contracts/schemas.md."""
    request_id: str
    response: str
    confidence: float = Field(ge=0.0, le=1.0, default=0.90)
    reasoning_summary: str = ""
    evidence: List[str] = Field(default_factory=list)
    recommendation: str = "review"  # approve | review | reject | escalate
    requires_human_review: bool = False
    telemetry: Optional[TelemetryMetadata] = None


class AuditEventPayload(BaseModel):
    """Structured audit payload for AI actions."""
    event_id: str
    request_id: str
    actor_id: Optional[int]
    actor_type: str
    action: str
    resource: str = "ai_engine"
    status: str  # success | fallback | error | safety_blocked
    telemetry: Optional[TelemetryMetadata] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ModelSpec(BaseModel):
    """Model specification entry in ModelRegistry."""
    model_id: str
    provider: str
    category: str = "LLM"  # LLM | REASONING_LLM | EMBEDDING_MODEL | VISION_MODEL | OCR_MODEL | RISK_MODEL | ANOMALY_MODEL | CLASSIFICATION_MODEL
    name: str
    capabilities: List[str]
    cost_per_1k_input_tokens: float = 0.0
    cost_per_1k_output_tokens: float = 0.0
    max_context_tokens: int = 128000
    recommended_tasks: List[str] = Field(default_factory=list)
