from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TrustFactorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    impact: str
    value: str
    description: str


class TrustProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    score: int = 700
    level: str = "good"
    change: int = 0
    factors: list[TrustFactorResponse] = Field(default_factory=list)
    updated_at: datetime


class RiskAssessmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    score: int
    level: str
    factors: Any
    evidence: Any
    recommendation: str
    confidence: Decimal
    created_at: datetime


class FraudSignalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    transaction_id: int | None = None
    type: str
    severity: str
    score: int
    evidence: Any
    status: str
    created_at: datetime
