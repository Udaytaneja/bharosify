from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
from ai.app.schemas.requests import AIExecutionRequest, AIExecutionResponse


class BaseProvider(ABC):
    """Abstract Base Class for all AI LLM Providers."""

    def __init__(self, provider_name: str, api_key: str | None = None):
        self.provider_name = provider_name
        self.api_key = api_key

    @abstractmethod
    async def generate(
        self,
        request: AIExecutionRequest,
        prompt_text: str,
        model_id: str,
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Executes generation on the provider.
        Returns:
            Tuple[response_text, raw_metadata_dict]
            raw_metadata_dict MUST contain:
            - prompt_tokens (int)
            - completion_tokens (int)
            - finish_reason (str)
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Checks if the provider has valid configuration / API keys."""
        pass
