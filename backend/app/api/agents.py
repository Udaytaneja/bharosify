import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.models.agent import AgentActionLogModel, AgentModel
from backend.app.models.user import User
from ai.app.schemas.agent_intelligence import (

    AgentActionEvaluationRequest,
    AgentActionEvaluationResponse,
    AgentProfileResponse,
    AgentRegistrationRequest,
)
from backend.app.services.agent_intelligence_service import AgentIntelligenceService

router = APIRouter(prefix="/agents", tags=["Agent Intelligence"])


@router.get("", response_model=List[AgentProfileResponse])
async def list_agents(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """List agents registered for the current user or organization."""
    res = await db.execute(select(AgentModel).where(AgentModel.owner_id == current_user.id))
    agents = res.scalars().all()
    
    # If no agent registered yet, auto-provision default Digital Twin & Underwriting agents
    if not agents:
        service = AgentIntelligenceService(db)
        a1 = await service.register_agent(
            agent_id="agent_dt_001",
            name="Financial Health Digital Twin Agent",
            owner_id=current_user.id,
            agent_type="digital_twin",
            capabilities=["Income/Expense Tracking", "Cash Flow Analysis", "Budget Optimization"],
            permissions=["financial_profile:read", "transactions:read"],
        )
        a2 = await service.register_agent(
            agent_id="agent_underwriting_002",
            name="Credit Risk & Underwriting Assister",
            owner_id=current_user.id,
            agent_type="underwriting",
            capabilities=["Loan Eligibility Pre-Check", "Repayment Capacity Estimation"],
            permissions=["financial_profile:read", "loan_application:read"],
        )
        agents = [a1, a2]

    return [
        AgentProfileResponse(
            id=a.id,
            name=a.name,
            owner_id=a.owner_id,
            organization_id=a.organization_id,
            agent_type=a.agent_type,
            status=a.status,
            trust_score=a.trust_score,
            risk_score=a.risk_score,
            capabilities=json.loads(a.capabilities),
            permissions=json.loads(a.permissions),
            policies=json.loads(a.policies),
        )
        for a in agents
    ]


@router.post("", response_model=AgentProfileResponse, status_code=status.HTTP_201_CREATED)
async def register_agent(
    payload: AgentRegistrationRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Register a new autonomous agent in the Agent Registry."""
    service = AgentIntelligenceService(db)
    agent = await service.register_agent(
        agent_id=payload.agent_id,
        name=payload.name,
        owner_id=current_user.id,
        organization_id=payload.organization_id,
        agent_type=payload.agent_type,
        capabilities=payload.capabilities,
        permissions=payload.permissions,
        policies=payload.policies,
    )
    return AgentProfileResponse(
        id=agent.id,
        name=agent.name,
        owner_id=agent.owner_id,
        organization_id=agent.organization_id,
        agent_type=agent.agent_type,
        status=agent.status,
        trust_score=agent.trust_score,
        risk_score=agent.risk_score,
        capabilities=json.loads(agent.capabilities),
        permissions=json.loads(agent.permissions),
        policies=json.loads(agent.policies),
    )


@router.get("/{agent_id}", response_model=AgentProfileResponse)
async def get_agent_profile(
    agent_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get detailed identity, trust score, risk score, and permissions for an agent."""
    service = AgentIntelligenceService(db)
    agent = await service.get_agent(agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "AGENT_NOT_FOUND", "message": f"Agent '{agent_id}' not found."},
        )
    return AgentProfileResponse(
        id=agent.id,
        name=agent.name,
        owner_id=agent.owner_id,
        organization_id=agent.organization_id,
        agent_type=agent.agent_type,
        status=agent.status,
        trust_score=agent.trust_score,
        risk_score=agent.risk_score,
        capabilities=json.loads(agent.capabilities),
        permissions=json.loads(agent.permissions),
        policies=json.loads(agent.policies),
    )


@router.put("/{agent_id}/status", response_model=AgentProfileResponse)
async def update_agent_status(
    agent_id: str,
    status_value: str = Query(..., alias="status"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update agent status (active, suspended, revoked)."""
    if status_value not in ["active", "pending", "suspended", "revoked"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "INVALID_STATUS", "message": f"Invalid status '{status_value}'."},
        )

    service = AgentIntelligenceService(db)
    agent = await service.update_agent_status(agent_id, status_value)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "AGENT_NOT_FOUND", "message": f"Agent '{agent_id}' not found."},
        )

    return AgentProfileResponse(
        id=agent.id,
        name=agent.name,
        owner_id=agent.owner_id,
        organization_id=agent.organization_id,
        agent_type=agent.agent_type,
        status=agent.status,
        trust_score=agent.trust_score,
        risk_score=agent.risk_score,
        capabilities=json.loads(agent.capabilities),
        permissions=json.loads(agent.permissions),
        policies=json.loads(agent.policies),
    )


@router.post("/evaluate", response_model=AgentActionEvaluationResponse)
async def evaluate_agent_action(
    payload: AgentActionEvaluationRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Evaluate an agent action request through the 9-stage evaluation pipeline."""
    service = AgentIntelligenceService(db)
    res = await service.evaluate_action(
        agent_id=payload.agent_id,
        action=payload.action,
        resource=payload.resource,
        tool_name=payload.tool_name,
        payload=payload.payload,
        actor_user_id=current_user.id,
        actor_role=current_user.role,
    )
    return AgentActionEvaluationResponse(**res)


@router.get("/{agent_id}/audit-log")
async def get_agent_audit_logs(
    agent_id: str,
    limit: int = Query(default=50, ge=1, le=200),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve audit history and explanations for an agent."""
    res = await db.execute(
        select(AgentActionLogModel)
        .where(AgentActionLogModel.agent_id == agent_id)
        .order_by(AgentActionLogModel.timestamp.desc())
        .limit(limit)
    )
    logs = res.scalars().all()
    return [
        {
            "id": l.id,
            "agent_id": l.agent_id,
            "action": l.action,
            "tool_name": l.tool_name,
            "resource": l.resource,
            "risk_level": l.risk_level,
            "decision": l.decision,
            "reason": l.reason,
            "audit_explanation": l.audit_explanation,
            "timestamp": l.timestamp.isoformat(),
        }
        for l in logs
    ]
