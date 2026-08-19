import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from backend.app.core.database import AsyncSessionLocal
from backend.app.main import app


@pytest.mark.asyncio
async def test_payment_infrastructure():
    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM users WHERE email = 'payuser@example.com';"))
        await session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register and login
        await client.post("/api/v1/auth/register", json={"name": "Pay User", "email": "payuser@example.com", "password": "Password123!"})
        l = await client.post("/api/v1/auth/login", json={"email": "payuser@example.com", "password": "Password123!"})
        h = {"Authorization": f"Bearer {l.json()['access_token']}"}

        # 1. Create payment (starts as pending)
        p_resp = await client.post(
            "/api/v1/payments",
            json={
                "amount": 250.00,
                "payment_reference": "PAY-REF-9999",
                "idempotency_key": "IDEM-KEY-9999",
            },
            headers=h,
        )
        assert p_resp.status_code == 201
        p_data = p_resp.json()
        p_id = p_data["id"]

        # 2. Idempotency test: resubmitting exact same key returns existing record
        p_idem = await client.post(
            "/api/v1/payments",
            json={
                "amount": 250.00,
                "payment_reference": "PAY-REF-9999",
                "idempotency_key": "IDEM-KEY-9999",
            },
            headers=h,
        )
        assert p_idem.status_code == 201
        assert p_idem.json()["id"] == p_id

        # 3. Explicit backend confirmation updates status to completed
        p_conf = await client.post(f"/api/v1/payments/{p_id}/confirm", headers=h)
        assert p_conf.status_code == 200
        assert p_conf.json()["status"] == "completed"
        assert p_conf.json()["reconciled"] is True

    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM users WHERE email = 'payuser@example.com';"))
        await session.commit()
