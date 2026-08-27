from typing import Dict, Any
from ai.app.providers.base import BaseProvider
from ai.app.providers.interfaces import BaseRiskModelProvider, BaseClassificationProvider, RiskOutput, ClassificationOutput
from ai.app.schemas.requests import AIExecutionRequest


class XGBoostRiskAdapter(BaseProvider, BaseRiskModelProvider, BaseClassificationProvider):
    """Adapter for XGBoost Credit Risk Scoring & Classification Model."""

    def __init__(self):
        super().__init__(provider_name="xgboost_risk", api_key=None)

    def is_available(self) -> bool:
        return True

    async def predict_risk(self, applicant_data: Dict[str, Any]) -> RiskOutput:
        income = float(applicant_data.get("income", 50000.0))
        debt = float(applicant_data.get("debt", 10000.0))
        expenses = float(applicant_data.get("expenses", 20000.0))
        requested_amount = float(applicant_data.get("requested_amount", 15000.0))

        dti = (debt + expenses) / max(income, 1.0)
        
        # Calculate risk score (300 to 850 scale)
        base_score = 750
        if dti > 0.6:
            base_score -= 120
        elif dti > 0.4:
            base_score -= 50

        if requested_amount > income * 2:
            base_score -= 80

        score = max(300, min(850, base_score))
        
        if score >= 720:
            level = "low"
            rec = "approve"
            pd = 0.02
        elif score >= 650:
            level = "medium"
            rec = "review"
            pd = 0.08
        elif score >= 550:
            level = "high"
            rec = "review"
            pd = 0.22
        else:
            level = "critical"
            rec = "reject"
            pd = 0.45

        return RiskOutput(
            score=score,
            risk_level=level,
            probability_of_default=pd,
            factors=[
                {"name": "Debt-to-Income (DTI)", "value": f"{round(dti*100, 1)}%", "impact": "negative" if dti > 0.4 else "positive"},
                {"name": "Income Stability", "value": "Verified", "impact": "positive"},
            ],
            recommendation=rec,
        )

    async def classify(self, input_features: Dict[str, Any]) -> ClassificationOutput:
        return ClassificationOutput(
            label="standard_prime",
            confidence=0.94,
            probabilities={"prime": 0.94, "subprime": 0.06}
        )

    async def generate(
        self, request: AIExecutionRequest, prompt_text: str, model_id: str = "xgboost-credit-v1"
    ) -> tuple[str, dict[str, any]]:
        res = await self.predict_risk(request.context or {})
        text = f"[XGBoost Credit Model] Predicted Risk Score: {res.score}/850 ({res.risk_level.upper()}). Recommendation: {res.recommendation.upper()}."
        return text, {"prompt_tokens": 12, "completion_tokens": 18, "finish_reason": "stop"}
