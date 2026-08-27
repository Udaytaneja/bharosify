import pytest
from ai.app.observability import metrics_calculator, ai_audit_logger
from ai.app.models import model_registry


def test_metrics_calculator():
    spec = model_registry.get_spec("gemini-1.5-flash")
    telemetry = metrics_calculator.compute(
        request_id="obs_req_1",
        task="chat",
        spec=spec,
        prompt_tokens=100,
        completion_tokens=200,
        latency_ms=150.5,
    )

    assert telemetry.request_id == "obs_req_1"
    assert telemetry.total_tokens == 300
    assert telemetry.cost_usd > 0.0
    assert telemetry.latency_ms == 150.5


def test_audit_logger():
    event = ai_audit_logger.log_event(
        request_id="audit_req_1",
        actor_id=5,
        actor_type="banker",
        action="ai_underwriting",
        status="success",
    )

    assert event.request_id == "audit_req_1"
    assert event.resource == "ai_engine"
    assert event.status == "success"
