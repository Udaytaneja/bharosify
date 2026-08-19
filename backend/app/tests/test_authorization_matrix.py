import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from backend.app.core.database import AsyncSessionLocal
from backend.app.main import app


@pytest.mark.asyncio
async def test_four_actor_authorization_matrix():
    """Verify complete isolation and authorization matrix between User A, User B, Banker A, and Banker B."""
    async with AsyncSessionLocal() as session:
        await session.execute(
            text("DELETE FROM users WHERE email LIKE '%_matrix@example.com';")
        )
        await session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register 4 actors
        rUA = await client.post("/api/v1/auth/register", json={"name": "User A", "email": "userA_matrix@example.com", "password": "Password123!"})
        assert rUA.status_code == 201
        uA_id = rUA.json()["id"]

        rUB = await client.post("/api/v1/auth/register", json={"name": "User B", "email": "userB_matrix@example.com", "password": "Password123!"})
        assert rUB.status_code == 201
        uB_id = rUB.json()["id"]

        rBA = await client.post("/api/v1/auth/register", json={"name": "Banker A", "email": "bankerA_matrix@example.com", "password": "Password123!"})
        assert rBA.status_code == 201
        bA_id = rBA.json()["id"]

        rBB = await client.post("/api/v1/auth/register", json={"name": "Banker B", "email": "bankerB_matrix@example.com", "password": "Password123!"})
        assert rBB.status_code == 201
        bB_id = rBB.json()["id"]

    # Set Banker A and Banker B roles in DB
    async with AsyncSessionLocal() as session:
        await session.execute(text(f"UPDATE users SET role = 'banker' WHERE id IN ({bA_id}, {bB_id});"))
        await session.commit()

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Login tokens
        lUA = await client.post("/api/v1/auth/login", json={"email": "userA_matrix@example.com", "password": "Password123!"})
        hUA = {"Authorization": f"Bearer {lUA.json()['access_token']}"}

        lUB = await client.post("/api/v1/auth/login", json={"email": "userB_matrix@example.com", "password": "Password123!"})
        hUB = {"Authorization": f"Bearer {lUB.json()['access_token']}"}

        lBA = await client.post("/api/v1/auth/login", json={"email": "bankerA_matrix@example.com", "password": "Password123!"})
        hBA = {"Authorization": f"Bearer {lBA.json()['access_token']}"}

        lBB = await client.post("/api/v1/auth/login", json={"email": "bankerB_matrix@example.com", "password": "Password123!"})
        hBB = {"Authorization": f"Bearer {lBB.json()['access_token']}"}

        # 1. Normal users forbidden from banker endpoints (403)
        res_b_cust = await client.get("/api/v1/bankers/customers", headers=hUA)
        assert res_b_cust.status_code == 403

        # 2. Banker A & B can access banker customers
        res_bA_cust = await client.get("/api/v1/bankers/customers", headers=hBA)
        assert res_bA_cust.status_code == 200

        res_bB_cust = await client.get("/api/v1/bankers/customers", headers=hBB)
        assert res_bB_cust.status_code == 200

        # 3. User A submits application
        app_A = await client.post(
            "/api/v1/applications",
            json={"amount": 15000.00, "purpose": "Renovation"},
            headers=hUA,
        )
        assert app_A.status_code == 201
        appA_id = app_A.json()["id"]

        # 4. User B tries to read User A's application -> 404/Forbidden
        app_B_tries_A = await client.get(f"/api/v1/applications/{appA_id}", headers=hUB)
        assert app_B_tries_A.status_code in (403, 404)

        # 5. User B tries to transition User A's application -> 404/Forbidden
        app_B_updates_A = await client.put(f"/api/v1/applications/{appA_id}", json={"status": "withdrawn"}, headers=hUB)
        assert app_B_updates_A.status_code in (403, 404)

        # 6. User A tries to approve their own application -> 400 (Only bankers can approve)
        userA_approves_self = await client.put(f"/api/v1/applications/{appA_id}", json={"status": "approved"}, headers=hUA)
        assert userA_approves_self.status_code == 400

        # 7. Banker A moves app through valid state transitions: submitted -> under_review -> underwriting -> approved
        await client.put(f"/api/v1/applications/{appA_id}", json={"status": "under_review"}, headers=hBA)
        await client.put(f"/api/v1/applications/{appA_id}", json={"status": "underwriting"}, headers=hBA)
        appA_approved = await client.put(f"/api/v1/applications/{appA_id}", json={"status": "approved"}, headers=hBA)
        assert appA_approved.status_code == 200

        # 8. Verify Loan created for User A
        loans_A = await client.get("/api/v1/loans", headers=hUA)
        assert loans_A.status_code == 200
        loanA_id = loans_A.json()[0]["id"]

        # 9. User B tries to view User A's loan -> 404
        loanB_views_A = await client.get(f"/api/v1/loans/{loanA_id}", headers=hUB)
        assert loanB_views_A.status_code == 404

        # 10. User B tries to view User A's repayment schedule -> 404
        repB_views_A = await client.get(f"/api/v1/repayments/{loanA_id}", headers=hUB)
        assert repB_views_A.status_code == 404

    async with AsyncSessionLocal() as session:
        await session.execute(
            text("DELETE FROM users WHERE email LIKE '%_matrix@example.com';")
        )
        await session.commit()
