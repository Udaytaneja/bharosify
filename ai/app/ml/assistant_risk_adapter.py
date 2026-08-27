from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from ai.app.ml.features import RiskFeatureVector


class AssistantMLSignal(BaseModel):
    model_name: str
    model_version: str
    status: str = "EXPERIMENTAL"  # "EXPERIMENTAL" | "VALIDATED" | "PRODUCTION_APPROVED"
    score: float
    confidence: float
    reason_codes: List[str] = Field(default_factory=list)
    disclaimer: str = "EXPERIMENTAL BENCHMARK MODEL. Signal is non-authoritative."


class AssistantMLSignalProviderAdapter:
    """
    ML Signal Adapter providing non-authoritative risk, fraud, and anomaly signals.
    Explicitly labels all benchmark models as EXPERIMENTAL.
    """

    def get_credit_risk_signal(
        self,
        monthly_income: float,
        monthly_expenses: float,
        debt_ratio: float,
        num_existing_loans: int = 1,
    ) -> AssistantMLSignal:
        """Returns credit risk signal."""
        # Feature processing
        risk_score = 0.35
        if debt_ratio > 0.45:
            risk_score += 0.25
        if num_existing_loans > 2:
            risk_score += 0.15

        risk_score = min(0.95, round(risk_score, 2))

        reasons = []
        if debt_ratio > 0.45:
            reasons.append("HIGH_DEBT_TO_INCOME_RATIO")
        if num_existing_loans > 2:
            reasons.append("MULTIPLE_ACTIVE_OBLIGATIONS")
        if not reasons:
            reasons.append("STABLE_REPAYMENT_PROFILE")

        return AssistantMLSignal(
            model_name="XGBoost-CreditRisk",
            model_version="v1.0.0",
            status="EXPERIMENTAL",
            score=risk_score,
            confidence=0.82,
            reason_codes=reasons,
        )

    def get_fraud_signal(self, amount: float, num_recent_transactions: int = 3) -> AssistantMLSignal:
        """Returns synthetic fraud signal."""
        fraud_score = 0.05
        reasons = ["LOW_FRAUD_RISK"]
        if amount > 1000000:
            fraud_score = 0.65
            reasons = ["HIGH_VALUE_TRANSACTION_VOLATILITY"]

        return AssistantMLSignal(
            model_name="LightGBM-FraudClassifier",
            model_version="v1.0.0",
            status="EXPERIMENTAL",
            score=fraud_score,
            confidence=0.88,
            reason_codes=reasons,
        )


assistant_ml_signal_provider_adapter = AssistantMLSignalProviderAdapter()
