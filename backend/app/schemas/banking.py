from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from backend.app.schemas.financial import FinancialHealthResponse
from backend.app.schemas.intelligence import TrustProfileResponse


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    phone: str | None = None
    account_status: str = "active"
    trust_profile: TrustProfileResponse | None = None
    financial_health: FinancialHealthResponse | None = None


class LoanApplicationCreate(BaseModel):
    amount: Decimal = Field(gt=0)
    purpose: str = Field(min_length=1, max_length=255)
    documents: list[Any] = Field(default_factory=list)


class LoanApplicationUpdate(BaseModel):
    purpose: str | None = Field(default=None, max_length=255)
    documents: list[Any] | None = None
    status: str | None = Field(
        default=None,
        pattern="^(draft|submitted|under_review|documents_required|underwriting|approved|rejected|withdrawn|completed)$",
    )


class LoanApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    amount: Decimal
    purpose: str
    status: str
    documents: list[Any]
    created_at: datetime
    updated_at: datetime


class UnderwritingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    application_id: int
    risk_score: int
    risk_level: str
    factors: Any
    evidence: Any
    recommendation: str
    confidence: Decimal
    human_review_required: bool
    decision: str


class LoanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    application_id: int
    customer_id: int
    principal: Decimal
    interest_rate: Decimal
    duration: int
    outstanding_amount: Decimal
    status: str
    start_date: datetime
    maturity_date: datetime


class RepaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    loan_id: int
    amount: Decimal
    due_date: datetime
    paid_date: datetime | None = None
    status: str
    payment_reference: str | None = None
