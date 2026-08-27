from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from ai.app.adapters.agent_intelligence_adapter import agent_intelligence_adapter
from ai.app.schemas.agent_intelligence import AgentActionEvaluationRequest, AgentActionEvaluationResponse
from ai.app.schemas.contracts.agent import AgentIntelligenceRequestDTO, AgentIntelligenceResponseDTO


class AIAgentIntelligence:
    """
    AI Agent Intelligence Orchestrator.
    Connects AI Gateway tool execution and Agent governance pipelines via contract adapters.
    """

    def __init__(self, db: Optional[AsyncSession] = None):
        self.db = db

    async def evaluate(self, request: AgentActionEvaluationRequest) -> AgentActionEvaluationResponse:
        dto_req = AgentIntelligenceRequestDTO(
            agent_id=request.agent_id,
            action=request.action,
            resource=request.resource,
            tool_name=request.tool_name,
            payload=request.payload or {},
        )

        dto_res: AgentIntelligenceResponseDTO = await agent_intelligence_adapter.evaluate_action(dto_req, db_session=self.db)

        return AgentActionEvaluationResponse(
            agent_id=dto_res.agent_id,
            action=dto_res.action,
            resource=dto_res.resource,
            decision=dto_res.decision,
            reason=dto_res.reason,
            risk_level=dto_res.risk_level,
            risk_score=dto_res.risk_score,
            trust_score=dto_res.trust_score,
            audit_explanation=dto_res.audit_explanation,
            evidence=dto_res.evidence,
            violations=dto_res.violations,
            anomalies=dto_res.anomalies,
            timestamp=dto_res.timestamp,
        )


ai_agent_intelligence = AIAgentIntelligence()
