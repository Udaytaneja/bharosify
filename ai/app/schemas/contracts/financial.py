from decimal import Decimal
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FinancialStateDTO(BaseModel):
    """Canonical contract DTO for customer financial state."""
    user_id: str = Field(description="User identifier")
    organization_id: Optional[str] = Field(default=None, description="Multi-tenant organization boundary")
    income: Decimal = Field(default=Decimal("100000.00"), description="Monthly income")
    expenses: Decimal = Field(default=Decimal("40000.00"), description="Monthly expenses")
    savings: Decimal = Field(default=Decimal("200000.00"), description="Liquid savings balance")
    existing_loans: Decimal = Field(default=Decimal("10000.00"), description="Existing monthly debt obligations")
    assets: Decimal = Field(default=Decimal("500000.00"), description="Total net assets")
    health_score: int = Field(default=94, ge=0, le=100, description="Financial health score 0-100")
    transactions: List[Dict[str, Any]] = Field(default_factory=list, description="Recent transaction list")


class FinancialCalculationResultDTO(BaseModel):
    """Canonical contract DTO for backend deterministic calculation results."""
    task: str = Field(description="Financial task e.g. EMI, repayment, affordability, digital_twin")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Exact backend metrics generated")
    calculated_by: str = Field(default="Backend-FinancialEngine", description="Authoritative engine tag")
    timestamp: str = Field(description="ISO timestamp")
