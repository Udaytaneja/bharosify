import time
from collections import defaultdict
from typing import Dict, List, Tuple

from ai.app.core.exceptions import SafetyViolationError


class SlidingWindowRateLimiter:
    """
    Sliding window rate limiter to protect against excessive model calls and Denial of Service.
    """

    def __init__(self, max_requests_per_window: int = 30, window_seconds: int = 60):
        self.max_requests = max_requests_per_window
        self.window_seconds = window_seconds
        self.requests_history: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, identifier: str) -> Tuple[bool, str]:
        """
        Checks if call is within rate limit window.
        Returns:
            Tuple[is_allowed, reason]
        """
        now = time.time()
        cutoff = now - self.window_seconds

        # Prune timestamps older than window
        timestamps = [t for t in self.requests_history[identifier] if t > cutoff]
        self.requests_history[identifier] = timestamps

        if len(timestamps) >= self.max_requests:
            return False, f"Rate limit exceeded: max {self.max_requests} requests per {self.window_seconds}s for identifier '{identifier}'."

        self.requests_history[identifier].append(now)
        return True, ""


class TokenBudgetManager:
    """
    Enforces prompt and completion token budgets to prevent model DoS and resource exhaustion.
    """

    def __init__(self, max_prompt_tokens: int = 8192, max_completion_tokens: int = 2048):
        self.max_prompt_tokens = max_prompt_tokens
        self.max_completion_tokens = max_completion_tokens

    def validate_budget(self, input_text: str, max_requested_completion_tokens: int = 2048) -> Tuple[bool, str]:
        """
        Estimates and validates token budgets.
        """
        # Rough token estimation (~4 chars per token)
        estimated_prompt_tokens = len(input_text) // 4
        if estimated_prompt_tokens > self.max_prompt_tokens:
            return False, f"Prompt token budget exceeded: estimated {estimated_prompt_tokens} tokens exceeds max {self.max_prompt_tokens}."

        if max_requested_completion_tokens > self.max_completion_tokens:
            return False, f"Completion token budget exceeded: requested {max_requested_completion_tokens} tokens exceeds max {self.max_completion_tokens}."

        return True, ""


rate_limiter = SlidingWindowRateLimiter()
token_budget_manager = TokenBudgetManager()
