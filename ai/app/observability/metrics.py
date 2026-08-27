from datetime import datetime
from ai.app.schemas.requests import TelemetryMetadata, ModelSpec


class MetricsCalculator:
    """Calculates observable telemetry metrics (token counts, cost USD, latency)."""

    def compute(
        self,
        request_id: str,
        task: str,
        spec: ModelSpec,
        prompt_tokens: int,
        completion_tokens: int,
        latency_ms: float,
        fallback_triggered: bool = False,
        retries_count: int = 0,
        pii_redacted: bool = False,
        prompt_shield_passed: bool = True,
        decision_guard_passed: bool = True,
    ) -> TelemetryMetadata:
        total_tokens = prompt_tokens + completion_tokens

        # Compute cost USD
        input_cost = (prompt_tokens / 1000.0) * spec.cost_per_1k_input_tokens
        output_cost = (completion_tokens / 1000.0) * spec.cost_per_1k_output_tokens
        total_cost_usd = round(input_cost + output_cost, 6)

        return TelemetryMetadata(
            request_id=request_id,
            task=task,
            model_id=spec.model_id,
            provider=spec.provider,
            fallback_triggered=fallback_triggered,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost_usd=total_cost_usd,
            latency_ms=round(latency_ms, 2),
            retries_count=retries_count,
            pii_redacted=pii_redacted,
            prompt_shield_passed=prompt_shield_passed,
            decision_guard_passed=decision_guard_passed,
            timestamp=datetime.utcnow(),
        )


metrics_calculator = MetricsCalculator()
