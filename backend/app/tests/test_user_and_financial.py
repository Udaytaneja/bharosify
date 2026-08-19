import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from backend.app.core.database import AsyncSessionLocal
from backend.app.main import app


@pytest.mark.asyncio
async def test_financial_and_cross_user_isolation():
    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM users WHERE email LIKE '%_fin@example.com';"))
        await session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register User A and User B
        rA = await client.post(
            "/api/v1/auth/register",
            json={"name": "User A", "email": "userA_fin@example.com", "password": "Password123!"},
        )
        assert rA.status_code == 201

        rB = await client.post(
            "/api/v1/auth/register",
            json={"name": "User B", "email": "userB_fin@example.com", "password": "Password123!"},
        )
        assert rB.status_code == 201

        # Login User A
        lA = await client.post("/api/v1/auth/login", json={"email": "userA_fin@example.com", "password": "Password123!"})
        tA = lA.json()["access_token"]
        hA = {"Authorization": f"Bearer {tA}"}

        # Login User B
        lB = await client.post("/api/v1/auth/login", json={"email": "userB_fin@example.com", "password": "Password123!"})
        tB = lB.json()["access_token"]
        hB = {"Authorization": f"Bearer {tB}"}

        # 1. Financial Profile GET / PUT
        fp_get = await client.get("/api/v1/financial/profile", headers=hA)
        assert fp_get.status_code == 200
        assert fp_get.json()["income"] == "0.00"

        fp_put = await client.put(
            "/api/v1/financial/profile",
            json={"income": 10000.00, "expenses": 3000.00, "savings": 5000.00},
            headers=hA,
        )
        assert fp_put.status_code == 200
        assert fp_put.json()["income"] == "10000.00"

        # 2. Financial Health GET
        fh_get = await client.get("/api/v1/financial/health", headers=hA)
        assert fh_get.status_code == 200
        assert fh_get.json()["score"] == 750

        # 3. Create transaction for User A
        txA = await client.post(
            "/api/v1/transactions",
            json={
                "amount": 500.00,
                "type": "expense",
                "category": "Groceries",
                "merchant": "Supermarket",
                "description": "Weekly food shopping",
            },
            headers=hA,
        )
        assert txA.status_code == 201
        txA_id = txA.json()["id"]

        # 4. Create transaction for User B
        txB = await client.post(
            "/api/v1/transactions",
            json={"amount": 1200.00, "type": "income", "category": "Salary"},
            headers=hB,
        )
        assert txB.status_code == 201

        # 5. Isolation Check: User A lists transactions (must only see txA, NOT txB)
        tx_listA = await client.get("/api/v1/transactions", headers=hA)
        assert tx_listA.status_code == 200
        tx_dataA = tx_listA.json()
        assert len(tx_dataA) == 1
        assert tx_dataA[0]["id"] == txA_id
        assert tx_dataA[0]["amount"] == "500.00"

        # User B lists transactions (must only see txB)
        tx_listB = await client.get("/api/v1/transactions", headers=hB)
        assert tx_listB.status_code == 200
        assert len(tx_listB.json()) == 1

    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM users WHERE email LIKE '%_fin@example.com';"))
        await session.commit()
