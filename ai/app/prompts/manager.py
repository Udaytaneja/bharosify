import json
import os
from typing import Dict, Tuple
from ai.app.prompts.templates import DEFAULT_PROMPTS


class PromptManager:
    """Prompt Versioning & Localization Manager."""

    def __init__(self, config_path: str = None):
        self._prompts: Dict[str, Dict[str, str]] = DEFAULT_PROMPTS
        if config_path and os.path.exists(config_path):
            self._load_from_config(config_path)

    def _load_from_config(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for task, val in data.items():
                    self._prompts[task] = val
        except Exception:
            pass

    def render(self, task: str, input_text: str, language: str = "en") -> Tuple[str, str]:
        """
        Renders the prompt for a task and language.
        Returns:
            Tuple[rendered_prompt_text, prompt_version]
        """
        task_prompts = self._prompts.get(task, self._prompts["chat"])
        version = task_prompts.get("version", "1.0.0")
        template = task_prompts.get(language, task_prompts.get("en", ""))
        
        rendered = template.format(input=input_text)
        return rendered, version


prompt_manager = PromptManager()
