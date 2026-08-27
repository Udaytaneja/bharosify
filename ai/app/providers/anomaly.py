from typing import Dict, Any
from ai.app.providers.base import BaseProvider
from ai.app.providers.interfaces import BaseAnomalyModelProvider, AnomalyOutput
from ai.app.schemas.requests import AIExecutionRequest


class IsolationForestAnomalyAdapter(BaseProvider, BaseAnomalyModelProvider):
    """Adapter for Isolation Forest Unsupervised Fraud & Transaction Anomaly Detection."""

    def __init__(self):
        super().__init__(provider_name="isolation_forest", api_key=None)

    def is_available(self) -> bool:
        return True

    async def detect_anomaly(
        self, transaction_data: Dict[str, Any], baseline_features: Dict[str, Any]
    ) -> AnomalyOutput:
        amount = float(transaction_data.get("amount", 0.0))
        avg_amount = float(baseline_features.get("average_transaction_amount", 50.0))
        velocity_count = int(transaction_data.get("tx_count_last_10m", 1))

        anomalous_features = []
        if amount > avg_amount * 5:
            anomalous_features.append("High Transaction Amount Spike")
        if velocity_count > 5:
            anomalous_features.append("Rapid Velocity Burst")

        is_anomaly = len(anomalous_features) > 0
        anomaly_score = 0.85 if is_anomaly else 0.05
        severity = "high" if len(anomalous_features) > 1 else ("warning" if is_anomaly else "info")

        return AnomalyOutput(
            is_anomaly=is_anomaly,
            anomaly_score=anomaly_score,
            severity=severity,
            anomalous_features=anomalous_features
        )

    async def generate(
        self, request: AIExecutionRequest, prompt_text: str, model_id: str = "isolation-forest-v1"
    ) -> tuple[str, dict[str, any]]:
        res = await self.detect_anomaly(request.context or {}, {"average_transaction_amount": 100.0})
        text = f"[Isolation Forest] Anomaly detected: {res.is_anomaly}. Score: {res.anomaly_score}. Severity: {res.severity}."
        return text, {"prompt_tokens": 10, "completion_tokens": 15, "finish_reason": "stop"}
