from decimal import Decimal
import pytest

from backend.app.services.financial_engine import FinancialEngine


def test_calculate_emi_precision():
    # Principal = 5,00,000, Rate = 12.5%, Tenure = 36 months
    res = FinancialEngine.calculate_emi(
        principal=Decimal("500000.00"),
        annual_rate_pct=Decimal("12.50"),
        tenure_months=36
    )

    assert res["principal"] == Decimal("500000.00")
    assert res["annual_rate_pct"] == Decimal("12.50")
    assert res["tenure_months"] == 36
    # Exact EMI check
    assert res["monthly_emi"] == Decimal("16726.81")
    assert res["total_payment"] == Decimal("602165.16")
    assert res["total_interest"] == Decimal("102165.16")


def test_repayment_schedule_sum():
    sched_data = FinancialEngine.calculate_repayment_schedule(
        principal=Decimal("100000.00"),
        annual_rate_pct=Decimal("10.00"),
        tenure_months=12
    )

    schedule = sched_data["schedule"]
    assert len(schedule) == 12

    total_principal_paid = sum(m["principal_payment"] for m in schedule)

    # Principal sum must equal original principal exactly
    assert total_principal_paid == Decimal("100000.00")
    assert schedule[-1]["remaining_balance"] == Decimal("0.00")


def test_debt_burden_and_foir():
    # Income = 1,00,000, Expenses = 30,000, Existing EMIs = 15,000
    db_res = FinancialEngine.calculate_debt_burden(
        monthly_income=Decimal("100000.00"),
        monthly_expenses=Decimal("30000.00"),
        existing_emis=Decimal("15000.00")
    )

    assert db_res["dti_ratio_pct"] == Decimal("15.00")
    assert db_res["foir_pct"] == Decimal("45.00")
    assert db_res["risk_category"] == "Moderate"
    assert db_res["disposable_income"] == Decimal("55000.00")


def test_affordability_max_loan():
    # Income = 1,00,000, Expenses = 30,000, Existing Debt = 10,000, Max FOIR = 50%
    # Max allowed obligations = 50,000 -> Max affordable EMI = 50,000 - 40,000 = 10,000
    aff = FinancialEngine.calculate_affordability(
        monthly_income=Decimal("100000.00"),
        monthly_expenses=Decimal("30000.00"),
        existing_emis=Decimal("10000.00"),
        proposed_annual_rate_pct=Decimal("12.50"),
        tenure_months=36,
        target_max_foir_pct=Decimal("50.00")
    )

    assert aff["max_affordable_emi"] == Decimal("10000.00")
    assert aff["is_affordable"] is True
    assert aff["max_loan_amount"] > Decimal("290000.00")


def test_loan_scenario_analysis():
    scenarios = [
        {"label": "Option A", "principal": 500000, "annual_rate_pct": 12.5, "tenure_months": 36},
        {"label": "Option B", "principal": 500000, "annual_rate_pct": 12.5, "tenure_months": 24},
        {"label": "Option C", "principal": 500000, "annual_rate_pct": 10.0, "tenure_months": 36},
    ]

    res = FinancialEngine.analyze_loan_scenarios(scenarios)
    assert len(res["scenarios"]) == 3
    # Option B (shorter tenure) should have lowest total interest
    assert res["lowest_interest_option"] == "Option B"
    # Option C (lower interest rate for same 36m) should have lower EMI than Option A
    assert res["scenarios"][2]["monthly_emi"] < res["scenarios"][0]["monthly_emi"]


def test_detect_financial_anomalies():
    txs = [
        {"id": "TX-1", "amount": 1000, "type": "expense", "merchant": "Grocery", "category": "Food"},
        {"id": "TX-2", "amount": 1000, "type": "expense", "merchant": "Grocery", "category": "Food"}, # Duplicate
        {"id": "TX-3", "amount": 100000, "type": "expense", "merchant": "Jewelry Shop", "category": "Shopping"}, # Spike
    ]

    anom = FinancialEngine.detect_financial_anomalies(txs, baseline_avg_monthly_expense=Decimal("5000.00"))
    assert anom["anomalies_detected"] is True
    assert anom["anomaly_count"] >= 2


def test_digital_twin_and_what_if():
    twin = FinancialEngine.get_digital_twin_state(
        savings=Decimal("200000.00"),
        monthly_income=Decimal("100000.00"),
        monthly_expenses=Decimal("40000.00"),
        existing_loans=Decimal("10000.00"),
        assets=Decimal("500000.00"),
        health_score=94
    )

    assert twin["net_worth"] == Decimal("690000.00")
    assert twin["monthly_surplus"] == Decimal("50000.00")

    # Simulate 15% salary increase
    sim = FinancialEngine.run_what_if_simulation(
        twin_state=twin,
        income_change_pct=Decimal("15.00"),
        expense_change_amount=Decimal("0.00"),
        new_loan_principal=Decimal("200000.00"),
        new_loan_rate_pct=Decimal("12.00"),
        new_loan_tenure_months=24
    )

    assert sim["simulated"]["monthly_income"] == Decimal("115000.00")
    assert sim["simulated"]["new_loan_emi"] > Decimal("0.00")
    assert sim["simulated"]["monthly_surplus"] > Decimal("0.00")
