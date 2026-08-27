from typing import Dict, Any
from ai.app.ml.interfaces import BaseRepaymentPredictionModel, RepaymentPredictionSignal, FeatureAttribution


class RepaymentPredictionModel(BaseRepaymentPredictionModel):
    """Repayment Likelihood & Delinquency Model (Logistic Regression Baseline)."""

    def __init__(self):
        self.version = "1.0.0"
        self.model_id = "ml-repayment-v1"

    async def predict_repayment(
        self, loan_features: Dict[str, Any], payment_history: Dict[str, Any]
    ) -> RepaymentPredictionSignal:
        income = float(loan_features.get("income", 50000.0))
        emi = float(loan_features.get("monthly_emi", 10000.0))
        past_ontime_ratio = float(payment_history.get("past_ontime_payment_ratio", 0.95))

        emi_burden = emi / max(income, 1.0)
        repayment_prob = max(0.05, min(0.99, (past_ontime_ratio * 0.75) + ((1.0 - emi_burden) * 0.25)))

        attributions = [
            FeatureAttribution(
                feature_name="past_ontime_payment_ratio",
                value=past_ontime_ratio,
                importance_weight=0.55,
                impact_direction="positive" if past_ontime_ratio > 0.85 else "negative",
                description=f"On-time payment ratio: {round(past_ontime_ratio*100, 1)}%",
            )
        ]

        if repayment_prob >= 0.90:
            tier = "on_time"
            delay_days = 0
        elif repayment_prob >= 0.70:
            tier = "30_days_late"
            delay_days = 15
        elif repayment_prob >= 0.50:
            tier = "60_days_late"
            delay_days = 45
        else:
            tier = "default_risk"
            delay_days = 90

        return RepaymentPredictionSignal(
            repayment_probability=round(repayment_prob, 4),
            expected_delay_days=delay_days,
            delinquency_tier=tier,
            confidence=0.90,
            attributions=attributions,
            model_version=self.version,
        )


repayment_prediction_model = RepaymentPredictionModel()
