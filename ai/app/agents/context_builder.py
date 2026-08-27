from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FinancialContextScope(BaseModel):
    """Specifies the MINIMUM REQUIRED DATA elements to fetch for an intent."""

    intent: str
    include_income: bool = False
    include_expenses: bool = False
    include_liabilities: bool = False
    include_loans: bool = False
    include_repayments: bool = False
    include_financial_health: bool = False
    include_transactions: bool = False
    include_ml_risk: bool = False
    include_rag_policy: bool = False


class FinancialContextBuilder:
    """
    Context Builder enforcing MINIMUM REQUIRED DATA scoping.
    Prevents fetching full customer profiles unnecessarily.
    """

    def build_scope(self, intent: str) -> FinancialContextScope:
        if intent == "LOAN_AFFORDABILITY":
            return FinancialContextScope(
                intent=intent,
                include_income=True,
                include_expenses=True,
                include_liabilities=True,
                include_loans=True,
                include_repayments=True,
                include_financial_health=False,
                include_ml_risk=True,
            )

        if intent == "REPAYMENT_QUERY":
            return FinancialContextScope(
                intent=intent,
                include_repayments=True,
                include_loans=True,
            )

        if intent == "FINANCIAL_HEALTH_EXPLANATION":
            return FinancialContextScope(
                intent=intent,
                include_income=True,
                include_expenses=True,
                include_liabilities=True,
                include_loans=True,
                include_financial_health=True,
                include_ml_risk=True,
            )

        if intent == "LOAN_SCENARIO":
            return FinancialContextScope(
                intent=intent,
                include_income=True,
                include_expenses=True,
                include_liabilities=True,
            )

        if intent == "RISK_EXPLANATION":
            return FinancialContextScope(
                intent=intent,
                include_income=True,
                include_liabilities=True,
                include_loans=True,
                include_repayments=True,
                include_ml_risk=True,
                include_rag_policy=True,
            )

        # Default minimal scope
        return FinancialContextScope(
            intent=intent,
            include_income=True,
            include_expenses=True,
        )


financial_context_builder = FinancialContextBuilder()
