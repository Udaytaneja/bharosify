import pytest
from ai.app.gateway import ai_gateway
from ai.app.schemas.requests import AIExecutionRequest, AIExecutionResponse


@pytest.mark.asyncio
async def test_gateway_execution_chat_english():
    request = AIExecutionRequest(
        request_id="test_req_001",
        user_id=1,
        role="user",
        task="chat",
        input="How do I improve my savings score?",
        language="en",
    )

    response = await ai_gateway.execute(request)
    assert isinstance(response, AIExecutionResponse)
    assert response.request_id == "test_req_001"
    assert len(response.response) > 0
    assert response.telemetry is not None
    assert response.telemetry.total_tokens > 0
    assert response.telemetry.latency_ms >= 0.0


@pytest.mark.asyncio
async def test_gateway_execution_scenario_hindi():
    request = AIExecutionRequest(
        request_id="test_req_002",
        user_id=2,
        role="user",
        task="scenario",
        input="अगर मैं ५०००० का लोन लूं तो क्या असर पड़ेगा?",
        language="hi",
    )

    response = await ai_gateway.execute(request)
    assert isinstance(response, AIExecutionResponse)
    assert response.request_id == "test_req_002"
    assert response.telemetry.task == "scenario"


@pytest.mark.asyncio
async def test_gateway_execution_underwriting_banker():
    request = AIExecutionRequest(
        request_id="test_req_003",
        user_id=10,
        role="banker",
        task="underwriting",
        input="Customer request for $10,000 personal loan",
        language="en",
    )

    response = await ai_gateway.execute(request)
    assert response.requires_human_review is True
    assert response.recommendation in ["approve", "review", "reject", "escalate"]
    assert "Non-authoritative" in response.reasoning_summary
