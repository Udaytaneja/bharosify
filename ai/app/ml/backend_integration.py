from typing import Any, Dict, List, Optional

from ai.app.ml.interfaces import FraudClassificationSignal, RiskPredictionSignal, TransactionAnomalySignal
from ai.app.schemas.contracts.fraud import FraudSignalDTO
from ai.app.schemas.contracts.risk import RiskAssessmentDTO
from ai.app.schemas.contracts.trust import TrustFactorDTO


class BackendMLIntegration:
    """
    Transforms AI ML signals into contract DTOs and provides conversion to backend ORMs via adapter.
    De-coupled from direct backend imports.
    """

    def to_risk_assessment_dto(self, customer_id: int, signal: RiskPredictionSignal) -> RiskAssessmentDTO:
        from ai.app.adapters.ml_adapter import backend_ml_integration_adapter

        return backend_ml_integration_adapter.to_risk_assessment_dto(customer_id, signal)

    def to_fraud_signal_dto(
        self, customer_id: int, transaction_id: Optional[int], signal: FraudClassificationSignal | TransactionAnomalySignal
    ) -> FraudSignalDTO:
        from ai.app.adapters.ml_adapter import backend_ml_integration_adapter

        return backend_ml_integration_adapter.to_fraud_signal_dto(customer_id, transaction_id, signal)

    def to_trust_factor_dtos(self, trust_profile_id: int, risk_signal: RiskPredictionSignal) -> List[TrustFactorDTO]:
        from ai.app.adapters.ml_adapter import backend_ml_integration_adapter

        return backend_ml_integration_adapter.to_trust_factor_dtos(trust_profile_id, risk_signal)

    def to_risk_assessment_model(self, customer_id: int, signal: RiskPredictionSignal) -> Any:
        from ai.app.adapters.ml_adapter import backend_ml_integration_adapter

        dto = self.to_risk_assessment_dto(customer_id, signal)
        return backend_ml_integration_adapter.to_risk_orm_model(dto)

    def to_fraud_signal_model(
        self, customer_id: int, transaction_id: Optional[int], signal: FraudClassificationSignal | TransactionAnomalySignal
    ) -> Any:
        from ai.app.adapters.ml_adapter import backend_ml_integration_adapter

        dto = self.to_fraud_signal_dto(customer_id, transaction_id, signal)
        return backend_ml_integration_adapter.to_fraud_orm_model(dto)

    def to_trust_factors(self, trust_profile_id: int, risk_signal: RiskPredictionSignal) -> List[Any]:
        from ai.app.adapters.ml_adapter import backend_ml_integration_adapter

        dtos = self.to_trust_factor_dtos(trust_profile_id, risk_signal)
        return backend_ml_integration_adapter.to_trust_orm_models(dtos)


backend_ml_integration = BackendMLIntegration()
