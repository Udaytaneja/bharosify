from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class FinancialProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    income: Decimal = Decimal("0.00")
    expenses: Decimal = Decimal("0.00")
    savings: Decimal = Decimal("0.00")
    assets: Decimal = Decimal("0.00")
    liabilities: Decimal = Decimal("0.00")
    existing_loans: Decimal = Decimal("0.00")


class FinancialProfileUpdate(BaseModel):
    income: Decimal | None = Field(default=None, ge=0)
    expenses: Decimal | None = Field(default=None, ge=0)
    savings: Decimal | None = Field(default=None, ge=0)
    assets: Decimal | None = Field(default=None, ge=0)
    liabilities: Decimal | None = Field(default=None, ge=0)
    existing_loans: Decimal | None = Field(default=None, ge=0)


class FinancialHealthResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    score: int = 750
    income: Decimal = Decimal("0.00")
    expenses: Decimal = Decimal("0.00")
    savings: Decimal = Decimal("0.00")
    debt: Decimal = Decimal("0.00")
    repayment_burden: Decimal = Decimal("0.00")
    status: str = "good"
    updated_at: datetime


class TransactionCreate(BaseModel):
    amount: Decimal = Field(gt=0)
    type: str = Field(pattern="^(income|expense|transfer)$")
    category: str = Field(min_length=1, max_length=50)
    merchant: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=255)
    date: datetime | None = None
    status: str = Field(default="completed", pattern="^(pending|completed|failed|reversed)$")


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    amount: Decimal
    type: str
    category: str
    merchant: str | None = None
    description: str | None = None
    date: datetime
    status: str
