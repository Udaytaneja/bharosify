import json
import urllib.request
import urllib.error
from typing import Dict, Any, Tuple
from ai.app.providers.base import BaseProvider
from ai.app.core.config import ai_settings
from ai.app.core.exceptions import ProviderAPIError
from ai.app.schemas.requests import AIExecutionRequest


class OpenAIProvider(BaseProvider):
    """OpenAI LLM Provider Adapter."""

    def __init__(self, api_key: str | None = None):
        key = api_key or ai_settings.openai_api_key or ai_settings.ai_api_key
        super().__init__(provider_name="openai", api_key=key)

    def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 0)

    async def generate(
        self,
        request: AIExecutionRequest,
        prompt_text: str,
        model_id: str = "gpt-4o-mini",
    ) -> Tuple[str, Dict[str, Any]]:
        if not self.is_available():
            raise ProviderAPIError("openai", "OpenAI API key is not configured.")

        url = "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": model_id,
            "messages": [
                {"role": "system", "content": "You are a financial AI assistant for AgentTrust OS."},
                {"role": "user", "content": prompt_text}
            ],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=ai_settings.timeout_seconds) as response:
                res_body = json.loads(response.read().decode("utf-8"))
                choices = res_body.get("choices", [])
                if not choices:
                    raise ProviderAPIError("openai", "No response choices returned by OpenAI.")
                
                text_content = choices[0].get("message", {}).get("content", "")
                usage = res_body.get("usage", {})

                meta = {
                    "prompt_tokens": usage.get("prompt_tokens", len(prompt_text.split())),
                    "completion_tokens": usage.get("completion_tokens", len(text_content.split())),
                    "finish_reason": choices[0].get("finish_reason", "stop"),
                    "provider": "openai",
                    "model_id": model_id,
                }
                return text_content, meta
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8") if e.fp else str(e)
            raise ProviderAPIError("openai", f"HTTP {e.code}: {err_msg}", status_code=e.code)
        except Exception as e:
            raise ProviderAPIError("openai", str(e), status_code=500)
