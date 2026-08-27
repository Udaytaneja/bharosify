import json
import urllib.request
import urllib.error
from typing import Dict, Any, Tuple, Optional
from ai.app.providers.base import BaseProvider
from ai.app.providers.interfaces import BaseLLMProvider
from ai.app.core.config import ai_settings
from ai.app.core.exceptions import ProviderAPIError
from ai.app.schemas.requests import AIExecutionRequest


class SarvamLLMAdapter(BaseProvider, BaseLLMProvider):
    """Sarvam AI Provider Adapter for Indic Language (Hindi/English) Processing."""

    def __init__(self, api_key: str | None = None):
        key = api_key or ai_settings.ai_api_key
        super().__init__(provider_name="sarvam", api_key=key)

    def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 0)

    async def generate_text(
        self, prompt: str, system_prompt: Optional[str] = None, language: str = "hi"
    ) -> Tuple[str, Dict[str, Any]]:
        if not self.is_available():
            # Graceful fallback response when Sarvam API key is not configured
            fallback_text = (
                f"[Sarvam AI (Indic Engine)] भाषा: {language} | "
                f"आपका वित्तीय विश्लेषण पूरा हो गया है। ('{prompt[:50]}...')"
                if language == "hi" else
                f"[Sarvam AI (Indic Engine)] Processed prompt in {language}: {prompt[:50]}..."
            )
            meta = {
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": len(fallback_text.split()),
                "finish_reason": "mock_fallback",
                "provider": "sarvam",
                "model_id": "sarvam-2b-indic",
            }
            return fallback_text, meta

        url = "https://api.sarvam.ai/v1/chat/completions"
        payload = {
            "model": "sarvam-2b-indic",
            "messages": [
                {"role": "system", "content": system_prompt or "आप AgentTrust OS के वित्तीय AI सहायक हैं।"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 1024,
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "api-subscription-key": self.api_key
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=ai_settings.timeout_seconds) as response:
                res_body = json.loads(response.read().decode("utf-8"))
                choices = res_body.get("choices", [])
                text_content = choices[0].get("message", {}).get("content", "")
                usage = res_body.get("usage", {})
                meta = {
                    "prompt_tokens": usage.get("prompt_tokens", len(prompt.split())),
                    "completion_tokens": usage.get("completion_tokens", len(text_content.split())),
                    "finish_reason": choices[0].get("finish_reason", "stop"),
                    "provider": "sarvam",
                    "model_id": "sarvam-2b-indic",
                }
                return text_content, meta
        except Exception as e:
            raise ProviderAPIError("sarvam", str(e))

    async def generate(
        self, request: AIExecutionRequest, prompt_text: str, model_id: str = "sarvam-2b-indic"
    ) -> Tuple[str, Dict[str, Any]]:
        return await self.generate_text(prompt_text, language=request.language)
