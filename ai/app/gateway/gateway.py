import asyncio
import time
import uuid
from typing import Dict, Any
from ai.app.core.config import ai_settings
from ai.app.core.exceptions import SafetyViolationError, ProviderAPIError
from ai.app.schemas.requests import AIExecutionRequest, AIExecutionResponse
from ai.app.routing.router import model_router
from ai.app.prompts.manager import prompt_manager
from ai.app.safety import ai_safety_layer, decision_guard
from ai.app.observability import metrics_calculator, ai_audit_logger
from ai.app.agents.financial_intelligence import FinancialIntelligenceService
from ai.app.schemas.financial_intelligence import FinancialIntelligenceRequest as FIRequest



FINANCIAL_TASKS = {
    "financial_intelligence",
    "financial_health",
    "affordability",
    "repayment",
    "loan_scenario",
    "anomaly_explanation",
    "digital_twin",
    "what_if_simulation",
}


class AIGateway:
    """Central AI Gateway orchestrating AI execution, safety, routing, retries, fallbacks, and telemetry."""

    async def execute(self, request: AIExecutionRequest) -> AIExecutionResponse:
        start_time = time.time()

        # 1. Ensure Request ID
        if not request.request_id:
            request.request_id = f"req_{uuid.uuid4().hex[:10]}"

        # 2. Unified Input Safety Layer (Injection, Token Budget, Rate Limit, Secret & PII Redaction)
        sanitized_input, pii_redacted, safety_flags = ai_safety_layer.validate_request_input(request)


        # Check if financial task
        if request.task in FINANCIAL_TASKS:
            fi_service = FinancialIntelligenceService()
            fi_req = FIRequest(
                request_id=request.request_id,
                user_id=request.user_id,
                query=sanitized_input,
                task=request.task,
                language=request.language,
                context=request.context or {},
            )
            fi_res = await fi_service.process_request(fi_req)

            latency_ms = (time.time() - start_time) * 1000.0
            primary_provider, primary_spec, _, _ = model_router.route(request)

            telemetry = metrics_calculator.compute(
                request_id=request.request_id,
                task=request.task,
                spec=primary_spec,
                prompt_tokens=len(sanitized_input.split()),
                completion_tokens=len(fi_res.explanation.split()),
                latency_ms=latency_ms,
                fallback_triggered=False,
                retries_count=0,
                pii_redacted=pii_redacted,
                prompt_shield_passed=True,
                decision_guard_passed=True,
            )

            execution_response = AIExecutionResponse(
                request_id=request.request_id,
                response=fi_res.explanation,
                confidence=fi_res.confidence,
                reasoning_summary=f"Processed deterministic financial intelligence for task '{fi_res.task}' in language '{fi_res.language}'.",
                evidence=fi_res.evidence,
                recommendation=fi_res.recommendation,
                requires_human_review=request.role == "banker" or fi_res.recommendation in ["review", "escalate"],
                telemetry=telemetry,
            )

            if ai_settings.decision_guard_enabled:
                execution_response = decision_guard.enforce(execution_response, role=request.role)

            ai_audit_logger.log_event(
                request_id=request.request_id,
                actor_id=request.user_id,
                actor_type=request.role,
                action=f"ai_{request.task}",
                status="success",
                telemetry=telemetry,
            )
            return execution_response

        # 4. Render Prompt with Versioning
        prompt_text, prompt_version = prompt_manager.render(
            task=request.task,
            input_text=sanitized_input,
            language=request.language
        )

        # 5. Route Model and Provider
        primary_provider, primary_spec, fallback_provider, fallback_spec = model_router.route(request)

        # 6. Execute with Retries & Fallback
        response_text = ""
        raw_meta: Dict[str, Any] = {}
        fallback_triggered = False
        retries_count = 0
        used_spec = primary_spec

        for attempt in range(ai_settings.max_retries + 1):
            try:
                # Execution with timeout handling
                response_text, raw_meta = await asyncio.wait_for(
                    primary_provider.generate(request, prompt_text, primary_spec.model_id),
                    timeout=ai_settings.timeout_seconds
                )
                break
            except Exception as e:
                retries_count = attempt + 1
                if attempt == ai_settings.max_retries:
                    # Fallback handling
                    fallback_triggered = True
                    used_spec = fallback_spec
                    try:
                        response_text, raw_meta = await fallback_provider.generate(
                            request, prompt_text, fallback_spec.model_id
                        )
                    except Exception as fallback_err:
                        response_text = f"[AI Engine Fallback] Unable to complete request for task '{request.task}'."
                        raw_meta = {
                            "prompt_tokens": len(prompt_text.split()),
                            "completion_tokens": len(response_text.split()),
                            "finish_reason": "error_fallback"
                        }
                else:
                    await asyncio.sleep(0.2 * (ai_settings.retry_backoff_factor ** attempt))

        latency_ms = (time.time() - start_time) * 1000.0

        # 7. Compute Telemetry Metrics
        telemetry = metrics_calculator.compute(
            request_id=request.request_id,
            task=request.task,
            spec=used_spec,
            prompt_tokens=raw_meta.get("prompt_tokens", len(prompt_text.split())),
            completion_tokens=raw_meta.get("completion_tokens", len(response_text.split())),
            latency_ms=latency_ms,
            fallback_triggered=fallback_triggered,
            retries_count=retries_count,
            pii_redacted=pii_redacted,
            prompt_shield_passed=True,
            decision_guard_passed=True,
        )

        # 8. Structured Response Construction
        requires_human = request.role == "banker" or request.task in ["risk_analysis", "underwriting"]
        recommendation = "approve" if request.role == "banker" and not fallback_triggered else "review"

        execution_response = AIExecutionResponse(
            request_id=request.request_id,
            response=response_text,
            confidence=0.88 if fallback_triggered else 0.95,
            reasoning_summary=f"Processed '{request.task}' using prompt v{prompt_version} ({used_spec.model_id}).",
            evidence=[f"Model: {used_spec.name}", f"Latency: {round(latency_ms, 1)}ms", f"Language: {request.language}"],
            recommendation=recommendation,
            requires_human_review=requires_human,
            telemetry=telemetry,
        )

        # 9. Unified Output Safety Layer (Decision Guard, Secret Leaks, Exfiltration, Financial Math Validation)
        execution_response = ai_safety_layer.validate_response_output(
            execution_response, role=request.role, ground_truth_metrics=request.context.get("ground_truth_metrics")
        )

        # 10. Log Structured Audit Event
        ai_audit_logger.log_event(
            request_id=request.request_id,
            actor_id=request.user_id,
            actor_type=request.role,
            action=f"ai_{request.task}",
            status="fallback" if fallback_triggered else "success",
            telemetry=telemetry,
        )

        return execution_response



ai_gateway = AIGateway()
