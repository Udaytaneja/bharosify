from typing import Any, Dict, List, Optional

from ai.app.ml.interfaces import FraudClassificationSignal, RiskPredictionSignal, TransactionAnomalySignal
from ai.app.schemas.contracts.fraud import FraudSignalDTO
from ai.app.schemas.contracts.risk import RiskAssessmentDTO
from ai.app.schemas.contracts.trust import TrustFactorDTO


class BackendMLIntegrationAdapter:
    """
    Backend ML Integration Adapter Port.
    Isolates Member 1's backend ORM models (RiskAssessment, FraudSignal, TrustFactor)
    behind clean contract DTO interfaces.
    """

    def to_risk_assessment_dto(self, customer_id: int, signal: RiskPredictionSignal) -> RiskAssessmentDTO:
        """Constructs a RiskAssessmentDTO contract instance from RiskPredictionSignal."""
        factors_payload = [attr.model_dump() for attr in signal.attributions]
        evidence_payload = {
            "model_version": signal.model_version,
            "probability_of_default": signal.probability_of_default,
            "confidence": signal.confidence,
        }

        return RiskAssessmentDTO(
            entity_id=str(customer_id),
            risk_score=signal.risk_score,
            probability_of_default=signal.probability_of_default,
            risk_level=signal.risk_level,
            confidence=signal.confidence,
            attributions=factors_payload,
            evidence=evidence_payload,
            recommendation=signal.suggested_decision,
            model_version=signal.model_version,
        )

    def to_fraud_signal_dto(
        self, customer_id: int, transaction_id: Optional[int], signal: FraudClassificationSignal | TransactionAnomalySignal
    ) -> FraudSignalDTO:
        """Constructs a FraudSignalDTO contract instance from Fraud/Anomaly signals."""
        if isinstance(signal, FraudClassificationSignal):
            fraud_type = signal.fraud_type
            severity = signal.severity
            score = int(signal.fraud_score * 100)
            evidence_payload = {
                "model_version": signal.model_version,
                "attributions": [attr.model_dump() for attr in signal.attributions],
            }
        else:
            fraud_type = "transaction_anomaly"
            severity = signal.severity
            score = int(signal.anomaly_score * 100)
            evidence_payload = {
                "model_version": signal.model_version,
                "anomalous_features": signal.anomalous_features,
            }

        return FraudSignalDTO(
            entity_id=str(customer_id),
            transaction_id=str(transaction_id) if transaction_id else None,
            fraud_type=fraud_type,
            severity=severity,
            score=score,
            evidence=evidence_payload,
            status="open",
            model_version=signal.model_version,
        )

    def to_trust_factor_dtos(self, trust_profile_id: int, risk_signal: RiskPredictionSignal) -> List[TrustFactorDTO]:
        """Constructs TrustFactorDTO contract instances based on ML attributions."""
        factors = []
        for attr in risk_signal.attributions:
            factor = TrustFactorDTO(
                trust_profile_id=str(trust_profile_id),
                name=attr.feature_name.replace("_", " ").title(),
                impact=attr.impact_direction,
                value=f"{round(attr.value, 2)}",
                description=attr.description,
            )
            factors.append(factor)
        return factors

    def to_risk_orm_model(self, dto: RiskAssessmentDTO) -> Any:
        """Constructs backend ORM instance from RiskAssessmentDTO when persistence is invoked."""
        from backend.app.models.risk import RiskAssessment

        return RiskAssessment(
            customer_id=int(dto.entity_id),
            score=dto.risk_score,
            level=dto.risk_level,
            factors=dto.attributions,
            evidence=dto.evidence,
            recommendation=dto.recommendation,
            confidence=dto.confidence,
        )

    def to_fraud_orm_model(self, dto: FraudSignalDTO) -> Any:
        """Constructs backend ORM instance from FraudSignalDTO when persistence is invoked."""
        from backend.app.models.fraud import FraudSignal

        return FraudSignal(
            customer_id=int(dto.entity_id),
            transaction_id=int(dto.transaction_id) if dto.transaction_id else None,
            type=dto.fraud_type,
            severity=dto.severity,
            score=dto.score,
            evidence=dto.evidence,
            status=dto.status,
        )

    def to_trust_orm_models(self, dtos: List[TrustFactorDTO]) -> List[Any]:
        """Constructs backend ORM instances from TrustFactorDTOs when persistence is invoked."""
        from backend.app.models.trust import TrustFactor

        models = []
        for dto in dtos:
            models.append(
                TrustFactor(
                    trust_profile_id=int(dto.trust_profile_id),
                    name=dto.name,
                    impact=dto.impact,
                    value=dto.value,
                    description=dto.description,
                )
            )
        return models


backend_ml_integration_adapter = BackendMLIntegrationAdapter()
