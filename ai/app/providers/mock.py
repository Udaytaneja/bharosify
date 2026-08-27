import json
from typing import Dict, Any, Tuple
from ai.app.providers.base import BaseProvider
from ai.app.schemas.requests import AIExecutionRequest


class MockProvider(BaseProvider):
    """Deterministic Fallback / Mock Provider for offline testing and failover."""

    def __init__(self):
        super().__init__(provider_name="mock", api_key="mock-key")

    def is_available(self) -> bool:
        return True

    async def generate(
        self,
        request: AIExecutionRequest,
        prompt_text: str,
        model_id: str = "mock-deterministic-v1",
    ) -> Tuple[str, Dict[str, Any]]:
        task = request.task
        lang = request.language
        role = request.role

        # Deterministic text generation based on task and language
        if task == "chat":
            if lang == "hi":
                text = f"[AI Engine (Mock)] आपके प्रश्न '{request.input}' का विश्लेषण पूर्ण हुआ। आपकी वित्तीय स्थिति स्थिर है।"
            else:
                text = f"[AI Engine (Mock)] Processed chat query: '{request.input}'. Your financial health score indicates stable performance."
        elif task == "scenario":
            if lang == "hi":
                text = f"[AI Engine (Mock)] परिदृश्य '{request.input}' का विश्लेषण: नकदी प्रवाह पर न्यूनतम प्रभाव पड़ेगा।"
            else:
                text = f"[AI Engine (Mock)] Scenario analysis for '{request.input}': Expected minor short-term liquidity drop, neutral long-term impact."
        elif task == "risk_analysis":
            text = f"[AI Risk Engine (Mock)] Risk assessment for banker query '{request.input}': Risk level is LOW (Score: 780/1000). Key evidence: On-time payments, low debt ratio."
        elif task == "underwriting":
            text = f"[AI Underwriting Engine (Mock)] Underwriting recommendation for '{request.input}': Recommendation: APPROVE. Confidence: 92%. DTI: 28%, Liquidity ratio: 3.2."
        else:
            text = f"[AI Engine (Mock)] Processed input for task '{task}': {request.input}"

        mock_metadata = {
            "prompt_tokens": len(prompt_text.split()),
            "completion_tokens": len(text.split()),
            "finish_reason": "stop",
            "provider": "mock",
            "model_id": model_id,
        }
        return text, mock_metadata
