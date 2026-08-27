import json
import os
from typing import Dict, List, Optional
from ai.app.schemas.requests import ModelSpec
from ai.app.core.exceptions import ModelNotFoundError

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "configs", "model_registry.json")

DEFAULT_SPECS = [
    ModelSpec(
        model_id="gemini-1.5-flash",
        provider="gemini",
        category="LLM",
        name="Google Gemini 1.5 Flash",
        capabilities=["chat", "scenario", "fast-inference"],
        cost_per_1k_input_tokens=0.000075,
        cost_per_1k_output_tokens=0.0003,
        max_context_tokens=1000000,
        recommended_tasks=["chat", "scenario"]
    ),
    ModelSpec(
        model_id="gemini-1.5-pro",
        provider="gemini",
        category="REASONING_LLM",
        name="Google Gemini 1.5 Pro",
        capabilities=["risk_analysis", "underwriting", "complex-reasoning"],
        cost_per_1k_input_tokens=0.00125,
        cost_per_1k_output_tokens=0.005,
        max_context_tokens=2000000,
        recommended_tasks=["risk_analysis", "underwriting"]
    ),
    ModelSpec(
        model_id="sarvam-2b-indic",
        provider="sarvam",
        category="LLM",
        name="Sarvam 2B Indic LLM",
        capabilities=["indic-nlp", "hindi-chat"],
        cost_per_1k_input_tokens=0.0001,
        cost_per_1k_output_tokens=0.0002,
        max_context_tokens=8192,
        recommended_tasks=["chat", "scenario"]
    ),
    ModelSpec(
        model_id="mock-deterministic-v1",
        provider="mock",
        category="LLM",
        name="Local Deterministic Mock Engine",
        capabilities=["chat", "scenario", "risk_analysis", "underwriting", "fallback"],
        cost_per_1k_input_tokens=0.0,
        cost_per_1k_output_tokens=0.0,
        max_context_tokens=32000,
        recommended_tasks=["fallback", "testing"]
    )
]


class ModelRegistry:
    """Registry maintaining metadata, pricing, and category mapping for registered models."""

    def __init__(self, config_path: Optional[str] = None):
        self._registry: Dict[str, ModelSpec] = {}
        self._load_defaults()
        path_to_load = config_path or DEFAULT_CONFIG_PATH
        if os.path.exists(path_to_load):
            self._load_from_json(path_to_load)

    def _load_defaults(self):
        for spec in DEFAULT_SPECS:
            self._registry[spec.model_id] = spec

    def _load_from_json(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data.get("models", []):
                    spec = ModelSpec(**item)
                    self._registry[spec.model_id] = spec
        except Exception:
            pass  # Fall back gracefully to defaults

    def get_spec(self, model_id: str) -> ModelSpec:
        if model_id not in self._registry:
            return self._registry.get(
                "mock-deterministic-v1",
                ModelSpec(
                    model_id=model_id,
                    provider="mock",
                    category="LLM",
                    name=model_id,
                    capabilities=["chat"],
                    cost_per_1k_input_tokens=0.0,
                    cost_per_1k_output_tokens=0.0
                )
            )
        return self._registry[model_id]

    def list_models(self) -> List[ModelSpec]:
        return list(self._registry.values())

    def get_models_by_category(self, category: str) -> List[ModelSpec]:
        return [
            spec for spec in self._registry.values()
            if spec.category.upper() == category.upper() or "fallback" in spec.capabilities
        ]

    def get_models_for_task(self, task: str) -> List[ModelSpec]:
        return [
            spec for spec in self._registry.values()
            if task in spec.recommended_tasks or "fallback" in spec.capabilities
        ]


# Singleton instance
model_registry = ModelRegistry()
