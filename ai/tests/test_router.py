import pytest
from ai.app.routing import model_router
from ai.app.models import model_registry
from ai.app.schemas.requests import AIExecutionRequest


def test_model_registry_defaults():
    models = model_registry.list_models()
    assert len(models) >= 4
    
    spec = model_registry.get_spec("gemini-1.5-flash")
    assert spec.provider == "gemini"
    assert spec.cost_per_1k_input_tokens > 0


def test_model_router_selection():
    request = AIExecutionRequest(
        request_id="req_router_1",
        user_id=1,
        role="banker",
        task="underwriting",
        input="Applicant evaluation context",
    )

    primary_prov, primary_spec, fallback_prov, fallback_spec = model_router.route(request)
    assert primary_prov is not None
    assert fallback_prov is not None
    assert fallback_spec.model_id == "mock-deterministic-v1"
