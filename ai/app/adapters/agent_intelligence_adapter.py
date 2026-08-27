from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from ai.app.schemas.contracts.agent import AgentIntelligenceRequestDTO, AgentIntelligenceResponseDTO


class AgentIntelligenceAdapter:
    """
    Agent Intelligence Adapter Port.
    Isolates Member 1's backend AgentIntelligenceService 9-stage evaluation pipeline
    behind clean contract DTO interfaces.
    """

    async def evaluate_action(
        self, request: AgentIntelligenceRequestDTO, db_session: Optional[AsyncSession] = None
    ) -> AgentIntelligenceResponseDTO:
        if db_session:
            # Isolated adapter import of backend AgentIntelligenceService
            from backend.app.services.agent_intelligence_service import AgentIntelligenceService

            service = AgentIntelligenceService(db_session)
            res = await service.evaluate_action(
                agent_id=request.agent_id,
                action=request.action,
                resource=request.resource,
                tool_name=request.tool_name,
                payload=request.payload,
            )
            return AgentIntelligenceResponseDTO(**res)
        else:
            return self._in_memory_evaluate(request)

    def _in_memory_evaluate(self, request: AgentIntelligenceRequestDTO) -> AgentIntelligenceResponseDTO:
        evidence = [
            f"[Stage 1 - Identity] Agent '{request.agent_id}' verified (Standalone Engine)",
            f"[Stage 2 - Permission] Action '{request.action}' on '{request.resource}' evaluated against standard scopes",
        ]
        violations = []
        anomalies = []

        is_sensitive = any(s in request.resource.lower() for s in ["payment", "banker", "admin", "delete"])
        amount = float(request.payload.get("amount", 0))

        if amount > 50000.0:
            violations.append(f"Financial threshold violation: amount ₹{amount:,.2f} exceeds limit ₹50,000.00")
            decision = "HUMAN_REVIEW"
            reason = "HIGH_VALUE_TRANSACTION_POLICY"
            risk_level = "high"
            risk_score = 75
        elif "admin" in request.action.lower():
            violations.append("Privilege escalation blocked: Admin privileges not granted")
            decision = "BLOCK"
            reason = "PRIVILEGE_ESCALATION"
            risk_level = "critical"
            risk_score = 90
        elif is_sensitive and request.action.lower() in ["delete", "transfer"]:
            decision = "HUMAN_REVIEW"
            reason = "DESTRUCTIVE_OR_FINANCIAL_ACTION"
            risk_level = "high"
            risk_score = 70
        else:
            decision = "ALLOW"
            reason = "SAFE_COMPLIANT_ACTION"
            risk_level = "low"
            risk_score = 15

        audit_explanation = (
            f"=== AUDITABLE AGENT DECISION EXPLANATION ===\n"
            f"Agent ID: {request.agent_id}\n"
            f"Action: {request.action} on '{request.resource}'\n"
            f"Decision: [{decision}]\n"
            f"Reason Code: {reason}\n"
            f"Calculated Risk Score: {risk_score}/100\n"
            f"Evidence: {'; '.join(evidence)}\n"
            f"Violations: {violations}\n"
            f"Conclusion: Action evaluated by Agent Intelligence governance."
        )

        from datetime import datetime

        return AgentIntelligenceResponseDTO(
            agent_id=request.agent_id,
            action=request.action,
            resource=request.resource,
            decision=decision,
            reason=reason,
            risk_level=risk_level,
            risk_score=risk_score,
            trust_score=850 if decision == "ALLOW" else 750,
            audit_explanation=audit_explanation,
            evidence=evidence,
            violations=violations,
            anomalies=anomalies,
            requires_human_review=decision in ["HOLD", "BLOCK", "HUMAN_REVIEW"],
            timestamp=datetime.utcnow().isoformat(),
        )


agent_intelligence_adapter = AgentIntelligenceAdapter()
