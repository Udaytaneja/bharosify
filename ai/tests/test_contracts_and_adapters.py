from decimal import Decimal
import pytest
from pydantic import ValidationError

from ai.app.adapters import (
    agent_intelligence_adapter,
    backend_ml_integration_adapter,
    financial_data_provider_adapter,
)
from ai.app.ml.interfaces import FeatureAttribution, FraudClassificationSignal, RiskPredictionSignal
from ai.app.schemas.contracts import (
    AgentIntelligenceRequestDTO,
    AgentIntelligenceResponseDTO,
    DocumentIntelligenceDTO,
    FinancialCalculationResultDTO,
    FinancialStateDTO,
    FraudAssessmentDTO,
    FraudSignalDTO,
    RiskAssessmentDTO,
    TrustFactorDTO,
)


def test_1_risk_assessment_dto_validation():
    dto = RiskAssessmentDTO(
        entity_id="101",
        risk_score=720,
        probability_of_default=0.04,
        risk_level="low",
        confidence=0.95,
        recommendation="approve",
    )
    assert dto.entity_id == "101"
    assert dto.risk_score == 720
    assert dto.probability_of_default == 0.04

    # Invalid risk score > 850
    with pytest.raises(ValidationError):
        RiskAssessmentDTO(
            entity_id="101",
            risk_score=999,  # Invalid
            probability_of_default=0.04,
            risk_level="low",
            confidence=0.95,
            recommendation="approve",
        )


def test_2_fraud_signal_dto_validation():
    dto = FraudSignalDTO(
        entity_id="user_55",
        fraud_type="velocity_spike",
        severity="high",
        score=85,
    )
    assert dto.entity_id == "user_55"
    assert dto.score == 85
    assert dto.status == "open"


def test_3_financial_state_dto_tenant_boundary():
    dto = FinancialStateDTO(
        user_id="user_12",
        organization_id="org_alpha",
        income=Decimal("150000.00"),
        expenses=Decimal("50000.00"),
    )
    assert dto.organization_id == "org_alpha"
    assert dto.income == Decimal("150000.00")


def test_4_agent_intelligence_contract_dto():
    req_dto = AgentIntelligenceRequestDTO(
        agent_id="agent_bot_99",
        organization_id="org_beta",
        action="transfer",
        resource="bank_account",
        payload={"amount": 75000.00},
    )
    assert req_dto.agent_id == "agent_bot_99"
    assert req_dto.organization_id == "org_beta"


@pytest.mark.asyncio
async def test_5_agent_adapter_in_memory_evaluation():
    req_dto = AgentIntelligenceRequestDTO(
        agent_id="agent_bot_99",
        action="transfer",
        resource="bank_account",
        payload={"amount": 75000.00},
    )

    res_dto: AgentIntelligenceResponseDTO = await agent_intelligence_adapter.evaluate_action(req_dto)
    assert res_dto.decision == "HUMAN_REVIEW"
    assert res_dto.risk_level == "high"
    assert len(res_dto.violations) > 0


@pytest.mark.asyncio
async def test_6_financial_adapter_deterministic_calculation():
    emi_res = financial_data_provider_adapter.calculate_emi(
        principal=Decimal("500000.00"), rate=Decimal("12.50"), tenure=36
    )
    assert float(emi_res["monthly_emi"]) == 16726.81


def test_7_ml_adapter_signal_to_dto_conversions():
    attr = FeatureAttribution(
        feature_name="dti_ratio",
        value=0.35,
        importance_weight=0.4,
        impact_direction="negative",
        description="High DTI",
    )
    risk_signal = RiskPredictionSignal(
        risk_score=710,
        probability_of_default=0.05,
        risk_level="low",
        confidence=0.92,
        attributions=[attr],
        suggested_decision="approve",
        model_version="1.0.0",
    )

    risk_dto = backend_ml_integration_adapter.to_risk_assessment_dto(customer_id=42, signal=risk_signal)
    assert risk_dto.entity_id == "42"
    assert risk_dto.risk_score == 710

    trust_dtos = backend_ml_integration_adapter.to_trust_factor_dtos(trust_profile_id=10, risk_signal=risk_signal)
    assert len(trust_dtos) == 1
    assert trust_dtos[0].name == "Dti Ratio"


def test_8_document_intelligence_dto():
    doc_dto = DocumentIntelligenceDTO(
        document_id="doc_771",
        organization_id="tenant_x",
        document_type="bank_statement",
        extracted_fields={"monthly_income": 120000},
        confidence=0.96,
    )
    assert doc_dto.document_id == "doc_771"
    assert doc_dto.organization_id == "tenant_x"
    assert doc_dto.validation_status == "valid"
