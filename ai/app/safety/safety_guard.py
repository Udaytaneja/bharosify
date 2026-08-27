from typing import Any, Dict, List, Optional, Tuple

from ai.app.core.exceptions import SafetyViolationError
from ai.app.safety.decision_guard import decision_guard, financial_value_validator, output_sanitizer, schema_validation_guard
from ai.app.safety.pii_sanitizer import pii_sanitizer, secret_detector
from ai.app.safety.prompt_shield import indirect_injection_scanner, malicious_doc_scanner, prompt_shield
from ai.app.safety.rate_limiter import rate_limiter, token_budget_manager
from ai.app.schemas.requests import AIExecutionRequest, AIExecutionResponse


class ToolAuthorizationGuard:
    """Validates tool call permissions before execution."""

    def authorize_tool(self, agent_id: str, tool_name: str, granted_tools: List[str]) -> Tuple[bool, str]:
        if "*" in granted_tools or "all" in granted_tools:
            return True, ""
        
        if tool_name in granted_tools:
            return True, ""

        return False, f"Unauthorized tool call: Agent '{agent_id}' does not have permission to execute tool '{tool_name}'."


class AISafetyLayer:
    """
    Unified AI Safety Layer enforcing comprehensive input/output validation,
    RAG authorization, tool authorization, rate limiting, and output verification.
    """

    def __init__(self):
        self.tool_guard = ToolAuthorizationGuard()

    def validate_request_input(self, request: AIExecutionRequest) -> Tuple[str, bool, List[str]]:
        """
        Executes pre-execution input safety checks.
        Returns:
            Tuple[sanitized_input_text, pii_redacted_bool, safety_flags]
        """
        safety_flags: List[str] = []

        # 1. Rate Limit Check
        identifier = f"user_{request.user_id}" if request.user_id else "anonymous"
        allowed, rate_reason = rate_limiter.is_allowed(identifier)
        if not allowed:
            raise SafetyViolationError("EXCESSIVE_MODEL_CALLS_RATE_LIMIT", rate_reason)

        # 2. Direct Prompt Injection Check
        is_safe, injection_reason = prompt_shield.validate(request.input)
        if not is_safe:
            raise SafetyViolationError("PROMPT_INJECTION_DETECTED", injection_reason)

        # 3. Token Budget Check
        budget_ok, budget_reason = token_budget_manager.validate_budget(request.input, request.max_tokens)
        if not budget_ok:
            raise SafetyViolationError("TOKEN_BUDGET_EXCEEDED", budget_reason)

        # 4. Secret Leakage Check in Input
        clean_input, secret_found, secret_labels = secret_detector.detect_and_redact(request.input)
        if secret_found:
            safety_flags.append(f"Secret leakage detected and redacted in input: {secret_labels}")

        # 5. PII Redaction
        sanitized_text, pii_redacted, _ = pii_sanitizer.sanitize(clean_input)
        if pii_redacted:
            safety_flags.append("PII detected and redacted in input.")

        return sanitized_text, pii_redacted or secret_found, safety_flags

    def validate_rag_chunks(self, chunks: List[Tuple[Any, float]], target_org_id: str, target_user_id: Optional[int]) -> List[Tuple[Any, float]]:
        """
        Enforces cross-tenant isolation and indirect prompt injection filtering on retrieved RAG chunks.
        """
        authorized_chunks = []
        for chunk, score in chunks:
            meta = getattr(chunk, "metadata", chunk)
            
            # Cross-Tenant Isolation
            org_id = getattr(meta, "organization_id", None) or (meta.get("organization_id") if isinstance(meta, dict) else None)
            if org_id and org_id != target_org_id:
                continue

            # Indirect Injection Filter
            text_content = getattr(chunk, "page_content", str(chunk))
            is_safe, _ = indirect_injection_scanner.scan_chunk(text_content, source_name="RAG Context")
            if not is_safe:
                continue

            authorized_chunks.append((chunk, score))

        return authorized_chunks

    def validate_document_content(self, text_content: str, filename: str = "document") -> Tuple[bool, str]:
        """
        Scans uploaded documents for malicious scripts or indirect injection vectors.
        """
        # Malicious code check
        is_clean, doc_reason = malicious_doc_scanner.scan_document(text_content, filename)
        if not is_clean:
            return False, doc_reason

        # Indirect injection check
        is_safe_inject, inject_reason = indirect_injection_scanner.scan_chunk(text_content, source_name=filename)
        if not is_safe_inject:
            return False, inject_reason

        return True, ""

    def validate_tool_call(self, agent_id: str, tool_name: str, granted_tools: List[str]) -> Tuple[bool, str]:
        """
        Verifies tool execution permission.
        """
        return self.tool_guard.authorize_tool(agent_id, tool_name, granted_tools)

    def validate_response_output(
        self, response: AIExecutionResponse, role: str, ground_truth_metrics: Optional[Dict[str, Any]] = None
    ) -> AIExecutionResponse:
        """
        Enforces post-execution output validation (decision guard, secret leaks, exfiltration, hallucinated financial values).
        Any output failing validation is NEVER allowed to silently enter a financial workflow.
        """
        validated_response = decision_guard.enforce(response, role=role, ground_truth_metrics=ground_truth_metrics)
        return validated_response


ai_safety_layer = AISafetyLayer()
