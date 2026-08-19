import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from backend.app.core.database import AsyncSessionLocal
from backend.app.main import app


@pytest.mark.asyncio
async def test_trust_audit_notifications_and_ai():
    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM users WHERE email = 'sysuser@example.com';"))
        await session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register user
        reg = await client.post(
            "/api/v1/auth/register",
            json={"name": "Sys User", "email": "sysuser@example.com", "password": "Password123!"},
        )
        assert reg.status_code == 201

        # Login
        log = await client.post("/api/v1/auth/login", json={"email": "sysuser@example.com", "password": "Password123!"})
        token = log.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 1. Trust endpoints
        tr_resp = await client.get("/api/v1/trust/me", headers=headers)
        assert tr_resp.status_code == 200
        assert tr_resp.json()["score"] == 720

        tf_resp = await client.get("/api/v1/trust/me/factors", headers=headers)
        assert tf_resp.status_code == 200
        assert len(tf_resp.json()) >= 1

        # 2. Notifications endpoint
        notif_resp = await client.get("/api/v1/notifications", headers=headers)
        assert notif_resp.status_code == 200

        # 3. AI assistant endpoint
        ai_resp = await client.post(
            "/api/v1/ai/chat",
            json={
                "request_id": "req-101",
                "task": "chat",
                "input": "How can I improve my financial health score?",
                "language": "en",
            },
            headers=headers,
        )
        assert ai_resp.status_code == 200
        ai_data = ai_resp.json()
        assert ai_data["request_id"] == "req-101"
        assert "[AI Engine Ready]" in ai_data["response"]

        # 4. Audit history GET /api/v1/audit/me
        audit_resp = await client.get("/api/v1/audit/me", headers=headers)
        assert audit_resp.status_code == 200
        audit_events = audit_resp.json()
        # Should record the AI chat call in audit log!
        assert len(audit_events) >= 1
        assert audit_events[0]["action"] == "ai_chat"

    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM users WHERE email = 'sysuser@example.com';"))
        await session.commit()
