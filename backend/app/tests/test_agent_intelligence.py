import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from backend.app.core.database import AsyncSessionLocal
from backend.app.main import app
from backend.app.services.agent_intelligence_service import AgentIntelligenceService


@pytest.mark.asyncio
async def test_agent_registration_and_identity_flow():
    async with AsyncSessionLocal() as db:
        await db.execute(text("DELETE FROM agent_action_logs WHERE agent_id = 'test_ag_001';"))
        await db.execute(text("DELETE FROM agents WHERE id = 'test_ag_001';"))
        await db.commit()

        service = AgentIntelligenceService(db)
        ag = await service.register_agent(
            agent_id="test_ag_001",
            name="Test Financial Digital Twin",
            owner_id=1,
            capabilities=["cash_flow_tracking", "spending_analysis"],
            permissions=["financial_profile:read", "transactions:read"],
        )

        assert ag.id == "test_ag_001"
        assert ag.status == "active"
        assert ag.trust_score == 850
        assert ag.risk_score == 15


@pytest.mark.asyncio
async def test_9_stage_pipeline_decisions():
    async with AsyncSessionLocal() as db:
        service = AgentIntelligenceService(db)

        # 1. ALLOW Decision: Safe, permitted action
        res_allow = await service.evaluate_action(
            agent_id="test_ag_001",
            action="read",
            resource="financial_profile",
            payload={"limit": 10},
        )
        assert res_allow["decision"] == "ALLOW"
        assert res_allow["reason"] == "SAFE_COMPLIANT_ACTION"
        assert "=== AUDITABLE AGENT DECISION EXPLANATION ===" in res_allow["audit_explanation"]

        # 2. BLOCK Decision: Ungranted privilege attempt
        res_block_perm = await service.evaluate_action(
            agent_id="test_ag_001",
            action="delete",
            resource="banker_underwriting",
            payload={},
        )
        assert res_block_perm["decision"] == "BLOCK"
        assert res_block_perm["reason"] in ["PRIVILEGE_VIOLATION", "PRIVILEGE_ESCALATION_BLOCKED"]
        assert len(res_block_perm["audit_explanation"]) > 50

        # 3. HUMAN_REVIEW Decision: High-value financial transfer policy violation
        res_hr = await service.evaluate_action(
            agent_id="test_ag_001",
            action="read",  # Permitted scope
            resource="financial_profile",
            payload={"amount": 150000.0},  # Exceeds 50k limit
        )
        assert res_hr["decision"] == "HUMAN_REVIEW"
        assert res_hr["reason"] == "HIGH_RISK_FINANCIAL_OR_DESTRUCTIVE_ACTION"
        assert any("exceeds max automated limit" in v for v in res_hr["violations"])
        assert "Escalated for mandatory human review" in res_hr["audit_explanation"]

        # 4. BLOCK Decision: Revoked Agent Status
        await service.update_agent_status("test_ag_001", "suspended")
        res_suspended = await service.evaluate_action(
            agent_id="test_ag_001",
            action="read",
            resource="financial_profile",
        )
        assert res_suspended["decision"] == "BLOCK"
        assert res_suspended["reason"] == "AGENT_STATUS_SUSPENDED"

        # Restore status for cleanup
        await service.update_agent_status("test_ag_001", "active")


@pytest.mark.asyncio
async def test_agent_api_endpoints():
    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM users WHERE email = 'agent_owner@example.com';"))
        await session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register User
        reg = await client.post(
            "/api/v1/auth/register",
            json={"name": "Agent Owner", "email": "agent_owner@example.com", "password": "Password123!"},
        )
        assert reg.status_code == 201

        # Login
        log = await client.post("/api/v1/auth/login", json={"email": "agent_owner@example.com", "password": "Password123!"})
        headers = {"Authorization": f"Bearer {log.json()['access_token']}"}

        # 1. List Agents
        list_res = await client.get("/api/v1/agents", headers=headers)
        assert list_res.status_code == 200
        agents_data = list_res.json()
        assert len(agents_data) >= 2  # Auto-provisioned default agents

        # 2. Register New Agent via API
        reg_ag = await client.post(
            "/api/v1/agents",
            json={
                "agent_id": "api_ag_101",
                "name": "API Automated Advisor Agent",
                "agent_type": "financial_advisor",
                "capabilities": ["Cash Flow Analysis"],
                "permissions": ["financial_profile:read"],
            },
            headers=headers,
        )
        assert reg_ag.status_code == 201
        assert reg_ag.json()["id"] == "api_ag_101"

        # 3. Get Agent Profile
        get_ag = await client.get("/api/v1/agents/api_ag_101", headers=headers)
        assert get_ag.status_code == 200
        assert get_ag.json()["trust_score"] == 850

        # 4. Evaluate Action via API
        eval_res = await client.post(
            "/api/v1/agents/evaluate",
            json={
                "agent_id": "api_ag_101",
                "action": "read",
                "resource": "financial_profile",
                "payload": {"amount": 2500.0},
            },
            headers=headers,
        )
        assert eval_res.status_code == 200
        eval_json = eval_res.json()
        assert eval_json["decision"] == "ALLOW"
        assert "AUDITABLE AGENT DECISION EXPLANATION" in eval_json["audit_explanation"]

        # 5. Retrieve Agent Audit Logs
        logs_res = await client.get("/api/v1/agents/api_ag_101/audit-log", headers=headers)
        assert logs_res.status_code == 200
        assert len(logs_res.json()) >= 1
        assert logs_res.json()[0]["decision"] == "ALLOW"

    # Cleanup
    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM agent_action_logs WHERE agent_id = 'api_ag_101';"))
        await session.execute(text("DELETE FROM agents WHERE id = 'api_ag_101';"))
        await session.execute(text("DELETE FROM users WHERE email = 'agent_owner@example.com';"))
        await session.commit()
