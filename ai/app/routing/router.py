from typing import Tuple
from ai.app.core.config import ai_settings
from ai.app.models.registry import model_registry
from ai.app.providers import (
    GeminiProvider, OpenAIProvider, MockProvider, BaseProvider,
    SarvamLLMAdapter, DocumentOCRAdapter, XGBoostRiskAdapter, IsolationForestAnomalyAdapter
)
from ai.app.schemas.requests import AIExecutionRequest, ModelSpec


class ModelRouter:
    """Dynamic Model Router selecting optimal provider & model for a task and language."""

    def __init__(self):
        self.providers = {
            "gemini": GeminiProvider(),
            "openai": OpenAIProvider(),
            "sarvam": SarvamLLMAdapter(),
            "ocr_engine": DocumentOCRAdapter(),
            "xgboost_risk": XGBoostRiskAdapter(),
            "isolation_forest": IsolationForestAnomalyAdapter(),
            "mock": MockProvider(),
        }

    def route(self, request: AIExecutionRequest) -> Tuple[BaseProvider, ModelSpec, BaseProvider, ModelSpec]:
        """
        Routes an execution request.
        Returns:
            Tuple[primary_provider, primary_spec, fallback_provider, fallback_spec]
        """
        task = request.task
        lang = request.language
        preferred_provider_name = ai_settings.default_provider

        # Routing rules by language & task
        if lang == "hi" and self.providers["sarvam"].is_available():
            target_model_id = "sarvam-2b-indic"
        elif task in ["risk_analysis", "underwriting"]:
            target_model_id = "xgboost-credit-v1" if preferred_provider_name == "xgboost_risk" else "gemini-1.5-pro"
        elif task == "ocr":
            target_model_id = "paddleocr-v4"
        elif task == "fraud_detection":
            target_model_id = "isolation-forest-v1"
        else:
            target_model_id = ai_settings.default_model

        primary_spec = model_registry.get_spec(target_model_id)
        primary_provider = self.providers.get(primary_spec.provider, self.providers["mock"])

        # Check if primary provider is available
        if not primary_provider.is_available():
            primary_spec = model_registry.get_spec("mock-deterministic-v1")
            primary_provider = self.providers["mock"]

        # Fallback provider configuration
        fallback_spec = model_registry.get_spec(ai_settings.fallback_model)
        fallback_provider = self.providers.get(fallback_spec.provider, self.providers["mock"])

        return primary_provider, primary_spec, fallback_provider, fallback_spec


model_router = ModelRouter()
