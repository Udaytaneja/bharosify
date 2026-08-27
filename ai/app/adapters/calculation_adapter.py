from decimal import Decimal
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class AffordabilityCalculationResult(BaseModel):
    requested_amount: Decimal
    tenure_years: int
    interest_rate_annual: Decimal = Decimal("12.5")
    monthly_income: Decimal
    monthly_expenses: Decimal
    calculated_emi: Decimal
    max_allowed_emi: Decimal
    new_dti_percent: Decimal
    remaining_disposable_income: Decimal
    is_affordable: bool
    status: str  # "AFFORDABLE" | "STRETCHED" | "UNAFFORDABLE"


class LoanScenarioCalculationResult(BaseModel):
    principal: Decimal
    tenure_years: int
    tenure_months: int
    annual_interest_rate_percent: Decimal = Decimal("12.5")
    monthly_emi: Decimal
    total_interest: Decimal
    total_repayment: Decimal
    dti_impact_percent: Decimal
    disposable_cashflow_after_emi: Decimal


class FinancialCalculationProviderAdapter:
    """
    Deterministic Financial Engine Adapter.
    Executes authoritative financial calculations (EMI, DTI, cash flow, affordability).
    The LLM NEVER performs financial arithmetic.
    """

    def calculate_affordability(
        self,
        monthly_income: Decimal,
        monthly_expenses: Decimal,
        requested_amount: Decimal = Decimal("500000"),
        tenure_years: int = 3,
        interest_rate_annual: Decimal = Decimal("12.5"),
    ) -> AffordabilityCalculationResult:
        n = tenure_years * 12
        r = (interest_rate_annual / Decimal("100")) / Decimal("12")

        # EMI Formula: P * r * (1+r)^n / ((1+r)^n - 1)
        r_float = float(r)
        p_float = float(requested_amount)
        if r_float > 0 and n > 0:
            emi_float = p_float * (r_float * (1 + r_float) ** n) / (((1 + r_float) ** n) - 1)
        else:
            emi_float = p_float / max(n, 1)

        calculated_emi = Decimal(str(round(emi_float, 2)))

        # Max allowed EMI = 50% of income - existing obligations
        max_allowed_emi = max(Decimal("0.00"), (monthly_income * Decimal("0.50")) - monthly_expenses)

        disposable_income = monthly_income - monthly_expenses - calculated_emi
        dti = ((monthly_expenses + calculated_emi) / max(monthly_income, Decimal("1.00"))) * Decimal("100")
        dti_rounded = Decimal(str(round(float(dti), 2)))

        is_affordable = calculated_emi <= max_allowed_emi and disposable_income > Decimal("0.00")
        status = "AFFORDABLE" if is_affordable else ("STRETCHED" if disposable_income > 0 else "UNAFFORDABLE")

        return AffordabilityCalculationResult(
            requested_amount=requested_amount,
            tenure_years=tenure_years,
            interest_rate_annual=interest_rate_annual,
            monthly_income=monthly_income,
            monthly_expenses=monthly_expenses,
            calculated_emi=calculated_emi,
            max_allowed_emi=max_allowed_emi,
            new_dti_percent=dti_rounded,
            remaining_disposable_income=disposable_income,
            is_affordable=is_affordable,
            status=status,
        )

    def calculate_loan_scenario(
        self,
        monthly_income: Decimal,
        monthly_expenses: Decimal,
        requested_amount: Decimal = Decimal("500000"),
        tenure_years: int = 3,
        interest_rate_annual: Decimal = Decimal("12.5"),
    ) -> LoanScenarioCalculationResult:
        n = tenure_years * 12
        r_float = float((interest_rate_annual / Decimal("100")) / Decimal("12"))
        p_float = float(requested_amount)

        if r_float > 0 and n > 0:
            emi_float = p_float * (r_float * (1 + r_float) ** n) / (((1 + r_float) ** n) - 1)
        else:
            emi_float = p_float / max(n, 1)

        monthly_emi = Decimal(str(round(emi_float, 2)))
        total_repayment = Decimal(str(round(emi_float * n, 2)))
        total_interest = total_repayment - requested_amount
        disposable = monthly_income - monthly_expenses - monthly_emi
        dti = ((monthly_expenses + monthly_emi) / max(monthly_income, Decimal("1.00"))) * Decimal("100")

        return LoanScenarioCalculationResult(
            principal=requested_amount,
            tenure_years=tenure_years,
            tenure_months=n,
            annual_interest_rate_percent=interest_rate_annual,
            monthly_emi=monthly_emi,
            total_interest=total_interest,
            total_repayment=total_repayment,
            dti_impact_percent=Decimal(str(round(float(dti), 2))),
            disposable_cashflow_after_emi=disposable,
        )


financial_calculation_provider_adapter = FinancialCalculationProviderAdapter()
