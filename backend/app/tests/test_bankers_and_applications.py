import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from backend.app.core.database import AsyncSessionLocal
from backend.app.main import app


@pytest.mark.asyncio
async def test_banker_system_and_loan_applications():
    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM users WHERE email IN ('customer1@example.com', 'banker1@example.com');"))
        await session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register normal user
        reg_c = await client.post(
            "/api/v1/auth/register",
            json={"name": "Customer One", "email": "customer1@example.com", "password": "Password123!"},
        )
        assert reg_c.status_code == 201
        c_id = reg_c.json()["id"]

        # Register banker user
        reg_b = await client.post(
            "/api/v1/auth/register",
            json={"name": "Banker One", "email": "banker1@example.com", "password": "Password123!"},
        )
        assert reg_b.status_code == 201
        b_id = reg_b.json()["id"]

    # Set banker role in DB
    async with AsyncSessionLocal() as session:
        await session.execute(text(f"UPDATE users SET role = 'banker' WHERE id = {b_id};"))
        await session.commit()

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Login customer & banker
        lc = await client.post("/api/v1/auth/login", json={"email": "customer1@example.com", "password": "Password123!"})
        tc = lc.json()["access_token"]
        hc = {"Authorization": f"Bearer {tc}"}

        lb = await client.post("/api/v1/auth/login", json={"email": "banker1@example.com", "password": "Password123!"})
        tb = lb.json()["access_token"]
        hb = {"Authorization": f"Bearer {tb}"}

        # 1. Role Protection Test: Customer accessing /api/v1/bankers/customers -> 403 Forbidden
        for_resp = await client.get("/api/v1/bankers/customers", headers=hc)
        assert for_resp.status_code == 403

        # 2. Banker accessing /api/v1/bankers/customers -> 200 OK
        bank_resp = await client.get("/api/v1/bankers/customers", headers=hb)
        assert bank_resp.status_code == 200
        customers = bank_resp.json()
        assert len(customers) >= 1

        # 3. Customer submits loan application
        app_resp = await client.post(
            "/api/v1/applications",
            json={"amount": 50000.00, "purpose": "Business Expansion", "documents": ["id_proof.pdf"]},
            headers=hc,
        )
        assert app_resp.status_code == 201
        app_data = app_resp.json()
        app_id = app_data["id"]
        assert app_data["status"] == "submitted"

        # 4. Banker reviews application and approves it through valid state machine:
        # submitted -> under_review -> underwriting -> approved
        r1 = await client.put(f"/api/v1/applications/{app_id}", json={"status": "under_review"}, headers=hb)
        assert r1.status_code == 200

        r2 = await client.put(f"/api/v1/applications/{app_id}", json={"status": "underwriting"}, headers=hb)
        assert r2.status_code == 200

        r3 = await client.put(f"/api/v1/applications/{app_id}", json={"status": "approved"}, headers=hb)
        assert r3.status_code == 200
        assert r3.json()["status"] == "approved"

        # 5. Verify active loan created automatically upon application approval
        loans_resp = await client.get("/api/v1/loans", headers=hc)
        assert loans_resp.status_code == 200
        loans = loans_resp.json()
        assert len(loans) == 1
        loan_id = loans[0]["id"]
        assert loans[0]["principal"] == "50000.00"

        # 6. Verify repayment schedule generated for loan
        reps_resp = await client.get(f"/api/v1/repayments/{loan_id}", headers=hc)
        assert reps_resp.status_code == 200
        repayments = reps_resp.json()
        assert len(repayments) == 12

    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM users WHERE email IN ('customer1@example.com', 'banker1@example.com');"))
        await session.commit()
