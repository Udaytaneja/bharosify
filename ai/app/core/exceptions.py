class AIServiceException(Exception):
    """Base exception for all AI subsystem errors."""
    def __init__(self, message: str, code: str = "AI_ERROR", details: dict = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


class ProviderAPIError(AIServiceException):
    """Raised when an external LLM API provider fails."""
    def __init__(self, provider: str, message: str, status_code: int = 500):
        super().__init__(
            message=f"Provider '{provider}' error: {message}",
            code="PROVIDER_API_ERROR",
            details={"provider": provider, "status_code": status_code},
        )


class ModelNotFoundError(AIServiceException):
    """Raised when a requested model is not registered."""
    def __init__(self, model_id: str):
        super().__init__(
            message=f"Model '{model_id}' was not found in the registry.",
            code="MODEL_NOT_FOUND",
            details={"model_id": model_id},
        )


class SafetyViolationError(AIServiceException):
    """Raised when a safety guardrail (e.g., prompt injection) is triggered."""
    def __init__(self, rule_name: str, message: str):
        super().__init__(
            message=f"Safety guardrail violation [{rule_name}]: {message}",
            code="SAFETY_VIOLATION",
            details={"rule_name": rule_name},
        )


class TimeoutError(AIServiceException):
    """Raised when execution times out."""
    def __init__(self, timeout_seconds: float):
        super().__init__(
            message=f"AI execution timed out after {timeout_seconds} seconds.",
            code="AI_TIMEOUT",
            details={"timeout_seconds": timeout_seconds},
        )


class ValidationException(AIServiceException):
    """Raised when structured AI output fails schema validation."""
    def __init__(self, message: str, errors: list = None):
        super().__init__(
            message=f"Output validation failed: {message}",
            code="OUTPUT_VALIDATION_ERROR",
            details={"errors": errors or []},
        )
