from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class PaymentCreate(BaseModel):
    amount: Decimal = Field(gt=0)
    payment_reference: str = Field(min_length=1, max_length=100)
    idempotency_key: str = Field(min_length=1, max_length=100)
    transaction_id: int | None = None
    repayment_id: int | None = None


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    amount: Decimal
    payment_reference: str
    idempotency_key: str
    status: str
    reconciled: bool
    created_at: datetime


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    recipient_id: int
    type: str
    title: str
    message: str
    read: bool
    created_at: datetime


class AuditEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    actor_id: int | None = None
    actor_type: str
    action: str
    resource: str
    resource_id: str | None = None
    result: str
    timestamp: datetime


class AIRequest(BaseModel):
    request_id: str = Field(min_length=1, max_length=100)
    task: str = Field(min_length=1, max_length=100)
    input: str = Field(min_length=1)
    language: str = Field(default="en")
    context: dict[str, Any] = Field(default_factory=dict)


class AIResponse(BaseModel):
    request_id: str
    response: str
    confidence: Decimal = Decimal("0.95")
    reasoning_summary: str
    evidence: list[Any] = Field(default_factory=list)
    recommendation: str = "review"
    requires_human_review: bool = False
