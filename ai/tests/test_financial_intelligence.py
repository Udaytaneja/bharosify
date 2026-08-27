import pytest
from decimal import Decimal

from ai.app.agents.financial_intelligence import FinancialIntelligenceService
from ai.app.schemas.financial_intelligence import FinancialIntelligenceRequest
from ai.app.gateway import ai_gateway
from ai.app.schemas.requests import AIExecutionRequest


@pytest.mark.asyncio
async def test_financial_health_explanation_hinglish():
    service = FinancialIntelligenceService()
    req = FinancialIntelligenceRequest(
        request_id="req_health_01",
        query="Mera financial health score aur monthly surplus kya hai?",
        task="financial_health",
        language="hinglish",
        context={
            "income": 100000.0,
            "expenses": 40000.0,
            "savings": 200000.0,
            "existing_loans": 10000.0,
            "health_score": 94,
        },
    )
    res = await service.process_request(req)

    assert res.request_id == "req_health_01"
    assert res.task == "financial_health"
    assert res.language == "hinglish"
    # Exact number check: 94/100 must be in explanation
    assert "94/100" in res.explanation
    assert "₹1,00,000.00" in res.explanation
    assert "₹40,000.00" in res.explanation
    assert len(res.evidence) > 0


@pytest.mark.asyncio
async def test_affordability_analysis_hindi():
    service = FinancialIntelligenceService()
    req = FinancialIntelligenceRequest(
        request_id="req_aff_01",
        query="क्या मैं ₹5,00,000 का लोन ले सकता हूँ?",
        task="affordability",
        language="hi",
        context={
            "income": 120000.0,
            "expenses": 35000.0,
            "existing_loans": 5000.0,
            "principal": 500000.0,
            "annual_rate_pct": 12.5,
            "tenure_months": 36,
        },
    )
    res = await service.process_request(req)

    assert res.task == "affordability"
    assert res.language == "hi"
    assert "50%" in res.explanation or "FOIR" in res.explanation
    assert res.recommendation in ["approve", "review", "advise"]
    assert "12.5%" in res.evidence[1] or "12.5%" in res.explanation


@pytest.mark.asyncio
async def test_repayment_analysis_exact_numbers_english():
    service = FinancialIntelligenceService()
    req = FinancialIntelligenceRequest(
        request_id="req_rep_01",
        query="What is my monthly EMI for ₹5,00,000 loan at 12.5% for 3 years?",
        task="repayment",
        language="en",
        context={
            "principal": 500000.0,
            "annual_rate_pct": 12.5,
            "tenure_months": 36,
        },
    )
    res = await service.process_request(req)

    assert res.task == "repayment"
    assert res.language == "en"
    # Exact numbers must be present
    assert "₹5,00,000.00" in res.explanation
    assert "12.5%" in res.explanation
    assert "₹16,726.81" in res.explanation
    assert "₹1,02,165.16" in res.explanation
    assert "₹6,02,165.16" in res.explanation


@pytest.mark.asyncio
async def test_loan_scenario_analysis():
    service = FinancialIntelligenceService()
    req = FinancialIntelligenceRequest(
        request_id="req_scen_01",
        query="Compare loan options for 5L loan at 12.5%",
        task="loan_scenario",
        language="en",
        context={
            "principal": 500000.0,
            "annual_rate_pct": 12.5,
            "tenure_months": 36,
        },
    )
    res = await service.process_request(req)

    assert res.task == "loan_scenario"
    assert "loan_scenarios" in res.deterministic_results
    assert len(res.evidence) >= 3


@pytest.mark.asyncio
async def test_anomaly_explanation():
    service = FinancialIntelligenceService()
    req = FinancialIntelligenceRequest(
        request_id="req_anom_01",
        query="Explain any suspicious spending or anomalies",
        task="anomaly_explanation",
        language="en",
        context={
            "transactions": [
                {"id": "T1", "amount": 100, "type": "expense", "merchant": "Uber"},
                {"id": "T2", "amount": 50000, "type": "expense", "merchant": "Luxury Store"}, # Spike
                {"id": "T3", "amount": 50000, "type": "expense", "merchant": "Luxury Store"}, # Duplicate
            ]
        },
    )
    res = await service.process_request(req)

    assert res.task == "anomaly_explanation"
    assert res.deterministic_results["anomalies"]["anomalies_detected"] is True
    assert res.recommendation in ["escalate", "review"]


@pytest.mark.asyncio
async def test_digital_twin_and_what_if_simulation():
    service = FinancialIntelligenceService()
    req = FinancialIntelligenceRequest(
        request_id="req_whatif_01",
        query="What if my salary increases by 15% and I take a 2L loan?",
        task="what_if_simulation",
        language="hinglish",
        context={
            "income": 100000.0,
            "expenses": 40000.0,
            "savings": 200000.0,
            "existing_loans": 10000.0,
            "principal": 200000.0,
            "annual_rate_pct": 12.0,
            "tenure_months": 24,
        },
    )
    res = await service.process_request(req)

    assert res.task == "what_if_simulation"
    assert res.what_if_result is not None
    assert "15%" in res.explanation
    assert res.digital_twin_state is not None


@pytest.mark.asyncio
async def test_gateway_execution_integration():
    req = AIExecutionRequest(
        request_id="req_gtw_01",
        user_id=1,
        role="user",
        task="financial_intelligence",
        input="Mera 5L loan par 12.5% rate se monthly EMI batayen 3 saal ke liye",
        language="hinglish",
        context={"principal": 500000, "annual_rate_pct": 12.5, "tenure_months": 36},
    )

    res = await ai_gateway.execute(req)
    assert res.request_id == "req_gtw_01"
    assert "₹16,726.81" in res.response
    assert len(res.evidence) > 0
    assert res.telemetry is not None
