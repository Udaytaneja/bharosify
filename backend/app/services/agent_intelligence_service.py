import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.agent import AgentActionLogModel, AgentModel, AgentPolicyModel
from backend.app.services.system_service import log_audit_event


class AgentIntelligenceService:
    """
    AgentTrust Agent Intelligence Service implementing the strict 9-Stage Evaluation Pipeline:
    1. Identity Verification
    2. Permission Check
    3. Context Analysis
    4. Behaviour Analysis
    5. Risk Scoring
    6. Policy Evaluation
    7. Recommendation Engine
    8. Final Decision (ALLOW | HOLD | BLOCK | HUMAN_REVIEW)
    9. Audit Logging & Explanation Generation
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_agent(self, agent_id: str) -> Optional[AgentModel]:
        res = await self.db.execute(select(AgentModel).where(AgentModel.id == agent_id))
        return res.scalar_one_or_none()

    async def register_agent(
        self,
        agent_id: str,
        name: str,
        owner_id: int,
        organization_id: str = "org_default",
        agent_type: str = "financial_advisor",
        capabilities: Optional[List[str]] = None,
        permissions: Optional[List[str]] = None,
        policies: Optional[List[str]] = None,
    ) -> AgentModel:
        existing = await self.get_agent(agent_id)
        if existing:
            return existing

        agent = AgentModel(
            id=agent_id,
            name=name,
            owner_id=owner_id,
            organization_id=organization_id,
            agent_type=agent_type,
            status="active",
            trust_score=850,
            risk_score=15,
            capabilities=json.dumps(capabilities or ["financial_analysis", "cash_flow_tracking"]),
            permissions=json.dumps(permissions or ["financial_profile:read", "transactions:read"]),
            policies=json.dumps(policies or ["max_amount_50k", "rate_limit_30m", "no_bulk_export"]),
        )
        self.db.add(agent)
        await self.db.commit()
        await self.db.refresh(agent)
        return agent

    async def update_agent_status(self, agent_id: str, new_status: str) -> Optional[AgentModel]:
        agent = await self.get_agent(agent_id)
        if not agent:
            return None
        agent.status = new_status
        agent.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(agent)
        return agent

    async def evaluate_action(
        self,
        agent_id: str,
        action: str,
        resource: str,
        tool_name: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
        actor_user_id: Optional[int] = None,
        actor_role: str = "user",
    ) -> Dict[str, Any]:
        """
        Executes the strict 9-Stage Evaluation Pipeline for an agent action request.
        """
        payload = payload or {}
        evidence: List[str] = []
        violations: List[str] = []
        anomalies: List[str] = []

        # STAGE 1: Identity Verification
        agent = await self.get_agent(agent_id)
        if not agent:
            # Auto-provision sandbox agent if not registered
            agent = await self.register_agent(
                agent_id=agent_id,
                name=f"Agent {agent_id}",
                owner_id=actor_user_id or 1,
            )

        evidence.append(f"[Stage 1 - Identity] Agent '{agent.id}' ({agent.name}), Status: {agent.status}, Owner: {agent.owner_id}")

        if agent.status in ["suspended", "revoked"]:
            explanation = f"Agent '{agent.id}' action BLOCKED because agent status is '{agent.status}'."
            return await self._finalize_decision(
                agent_id=agent.id,
                action=action,
                tool_name=tool_name,
                resource=resource,
                risk_level="critical",
                decision="BLOCK",
                reason=f"AGENT_STATUS_{agent.status.upper()}",
                audit_explanation=explanation,
                evidence=evidence,
                trust_score=agent.trust_score,
                risk_score=95,
            )

        # STAGE 2: Permission & Scope Check
        granted_permissions = json.loads(agent.permissions)
        has_permission = self._check_permission(action, resource, granted_permissions)
        evidence.append(f"[Stage 2 - Permission] Requested Action: '{action}' on '{resource}'. Granted Scopes: {granted_permissions}. Result: {'ALLOWED' if has_permission else 'DENIED'}")

        if not has_permission:
            explanation = f"Agent '{agent.id}' attempted ungranted action '{action}' on resource '{resource}'. Blocked due to privilege boundary violation."
            return await self._finalize_decision(
                agent_id=agent.id,
                action=action,
                tool_name=tool_name,
                resource=resource,
                risk_level="high",
                decision="BLOCK",
                reason="PRIVILEGE_VIOLATION",
                audit_explanation=explanation,
                evidence=evidence,
                trust_score=max(100, agent.trust_score - 50),
                risk_score=85,
            )

        # STAGE 3: Context Analysis
        is_sensitive_resource = any(s in resource.lower() for s in ["payment", "banker", "underwriting", "admin", "delete", "user_role"])
        data_volume = int(payload.get("limit", payload.get("count", 1)))
        evidence.append(f"[Stage 3 - Context] Resource Sensitivity: {'HIGH' if is_sensitive_resource else 'NORMAL'}, Data Volume requested: {data_volume}")

        # STAGE 4: Behaviour Analysis & Anomaly Detection
        call_count_1m, failure_count_10m = await self._get_agent_metrics(agent.id)
        evidence.append(f"[Stage 4 - Behaviour] 1-min Call Frequency: {call_count_1m}/min, 10-min Failure Count: {failure_count_10m}")

        if call_count_1m > 30:
            anomalies.append("Call frequency burst detected (>30 calls/min)")
        if failure_count_10m > 5:
            anomalies.append("High recent failure count (>5 failures in 10 mins)")

        # Check privilege escalation / admin access attempt
        if "admin" in action.lower() or "role" in action.lower():
            if actor_role != "admin" and "admin" not in granted_permissions:
                violations.append("Privilege escalation attempt: Non-admin agent attempting admin operation.")

        # Check bulk data access
        if data_volume > 100:
            anomalies.append(f"Unusual bulk data access request ({data_volume} items)")

        # STAGE 5: Risk Scoring (0-100)
        base_risk = 10
        if is_sensitive_resource:
            base_risk += 35
        if action.lower() in ["delete", "drop", "update_role", "transfer"]:
            base_risk += 40
        if anomalies:
            base_risk += len(anomalies) * 15
        if violations:
            base_risk += len(violations) * 25

        calculated_risk_score = min(100, base_risk)
        risk_level = "low"
        if calculated_risk_score >= 80:
            risk_level = "critical"
        elif calculated_risk_score >= 60:
            risk_level = "high"
        elif calculated_risk_score >= 35:
            risk_level = "medium"

        evidence.append(f"[Stage 5 - Risk Scoring] Calculated Action Risk Score: {calculated_risk_score}/100 ({risk_level.upper()})")

        # STAGE 6: Policy Evaluation
        monetary_amount = float(payload.get("amount", payload.get("transfer_amount", 0)))
        if monetary_amount > 50000.0:
            violations.append(f"Financial threshold policy violation: Requested amount ₹{monetary_amount:,.2f} exceeds max automated limit of ₹50,000.00.")

        evidence.append(f"[Stage 6 - Policy Evaluation] Active Violations: {violations if violations else 'None'}. Active Anomalies: {anomalies if anomalies else 'None'}")

        # STAGE 7 & 8: Recommendation Engine & Final Decision
        if any("Privilege escalation" in v for v in violations):
            decision = "BLOCK"
            reason = "PRIVILEGE_ESCALATION_BLOCKED"
        elif any("exceeds max automated limit" in v for v in violations) or action.lower() in ["payment_execution", "bulk_delete"]:
            decision = "HUMAN_REVIEW"
            reason = "HIGH_RISK_FINANCIAL_OR_DESTRUCTIVE_ACTION"
        elif call_count_1m > 30:
            decision = "HOLD"
            reason = "RATE_LIMIT_COOLDOWN_REQUIRED"
        elif risk_level in ["high", "critical"] and is_sensitive_resource:
            decision = "HUMAN_REVIEW"
            reason = "SENSITIVE_RESOURCE_HIGH_RISK"
        else:
            decision = "ALLOW"
            reason = "SAFE_COMPLIANT_ACTION"

        # STAGE 9: Audit Logging & Auditable Explanation
        audit_explanation = self._build_audit_explanation(
            agent_id=agent.id,
            action=action,
            resource=resource,
            decision=decision,
            reason=reason,
            risk_score=calculated_risk_score,
            evidence=evidence,
            violations=violations,
            anomalies=anomalies,
        )

        # Update dynamic agent metrics in database
        new_trust = agent.trust_score
        if decision == "ALLOW":
            new_trust = min(1000, agent.trust_score + 2)
        elif decision in ["BLOCK", "HUMAN_REVIEW"]:
            new_trust = max(100, agent.trust_score - 15)

        agent.trust_score = new_trust
        agent.risk_score = calculated_risk_score
        await self.db.commit()

        return await self._finalize_decision(
            agent_id=agent.id,
            action=action,
            tool_name=tool_name,
            resource=resource,
            risk_level=risk_level,
            decision=decision,
            reason=reason,
            audit_explanation=audit_explanation,
            evidence=evidence,
            trust_score=new_trust,
            risk_score=calculated_risk_score,
            violations=violations,
            anomalies=anomalies,
        )

    def _check_permission(self, action: str, resource: str, permissions: List[str]) -> bool:
        if "*" in permissions or "all" in permissions:
            return True
        
        target = f"{resource}:{action}"
        for perm in permissions:
            if perm == target or perm == f"{resource}:*" or perm == f"*:{action}":
                return True
            # Substring key match (e.g. "financial_profile" in perm)
            if resource in perm or perm in resource:
                return True
        return False

    async def _get_agent_metrics(self, agent_id: str) -> Tuple[int, int]:
        one_min_ago = datetime.utcnow() - timedelta(minutes=1)
        ten_min_ago = datetime.utcnow() - timedelta(minutes=10)

        res_1m = await self.db.execute(
            select(func.count(AgentActionLogModel.id)).where(
                AgentActionLogModel.agent_id == agent_id,
                AgentActionLogModel.timestamp >= one_min_ago,
            )
        )
        count_1m = res_1m.scalar() or 0

        res_fails = await self.db.execute(
            select(func.count(AgentActionLogModel.id)).where(
                AgentActionLogModel.agent_id == agent_id,
                AgentActionLogModel.timestamp >= ten_min_ago,
                AgentActionLogModel.decision.in_(["BLOCK", "HOLD"]),
            )
        )
        fails_10m = res_fails.scalar() or 0

        return count_1m, fails_10m

    def _build_audit_explanation(
        self,
        agent_id: str,
        action: str,
        resource: str,
        decision: str,
        reason: str,
        risk_score: int,
        evidence: List[str],
        violations: List[str],
        anomalies: List[str],
    ) -> str:
        timestamp_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        lines = [
            f"=== AUDITABLE AGENT DECISION EXPLANATION ===",
            f"Timestamp: {timestamp_str}",
            f"Agent ID: {agent_id}",
            f"Target Action: {action} on resource '{resource}'",
            f"Final Governance Decision: [{decision}]",
            f"Decision Reason Code: {reason}",
            f"Calculated Action Risk Score: {risk_score}/100",
            f"Governance Pipeline Stages Summary:",
        ]
        lines.extend([f"  - {e}" for e in evidence])

        if violations:
            lines.append("Detected Policy Violations:")
            lines.extend([f"  ! [VIOLATION] {v}" for v in violations])

        if anomalies:
            lines.append("Detected Behavioural Anomalies:")
            lines.extend([f"  ! [ANOMALY] {a}" for a in anomalies])

        if decision == "ALLOW":
            lines.append("Conclusion: Action verified against identity, permission, and security policy rules. Executed safely.")
        elif decision == "HUMAN_REVIEW":
            lines.append("Conclusion: Action involves high financial or sensitive resource risks exceeding automated bounds. Escalated for mandatory human review.")
        elif decision == "HOLD":
            lines.append("Conclusion: Action triggered a rate burst or frequency warning. Temporarily held for cooldown.")
        else:
            lines.append("Conclusion: Action violated security policy or privilege boundaries. Blocked by backend governance.")

        return "\n".join(lines)

    async def _finalize_decision(
        self,
        agent_id: str,
        action: str,
        tool_name: Optional[str],
        resource: str,
        risk_level: str,
        decision: str,
        reason: str,
        audit_explanation: str,
        evidence: List[str],
        trust_score: int,
        risk_score: int,
        violations: Optional[List[str]] = None,
        anomalies: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        log_entry = AgentActionLogModel(
            agent_id=agent_id,
            action=action,
            tool_name=tool_name,
            resource=resource,
            risk_level=risk_level,
            decision=decision,
            reason=reason,
            audit_explanation=audit_explanation,
            timestamp=datetime.utcnow(),
        )
        self.db.add(log_entry)
        await self.db.commit()

        # Log system audit event
        await log_audit_event(
            db=self.db,
            actor_id=None,
            actor_type="agent",
            action=f"agent_action_{decision.lower()}",
            resource=f"agent:{agent_id}",
            resource_id=resource,
            result=decision.lower(),
        )

        return {
            "agent_id": agent_id,
            "action": action,
            "resource": resource,
            "decision": decision,  # ALLOW | HOLD | BLOCK | HUMAN_REVIEW
            "reason": reason,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "trust_score": trust_score,
            "audit_explanation": audit_explanation,
            "evidence": evidence,
            "violations": violations or [],
            "anomalies": anomalies or [],
            "timestamp": datetime.utcnow().isoformat(),
        }
