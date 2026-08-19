import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from backend.app.core.database import AsyncSessionLocal
from backend.app.main import app


@pytest.mark.asyncio
async def test_user_profile_endpoints():
    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM users WHERE email = 'test-profile@example.com';"))
        await session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register user
        reg_resp = await client.post(
            "/api/v1/auth/register",
            json={
                "name": "Profile User",
                "email": "test-profile@example.com",
                "password": "Password123!",
                "phone": "9998887770",
                "language": "en",
            },
        )
        assert reg_resp.status_code == 201

        # Login
        login_resp = await client.post(
            "/api/v1/auth/login",
            json={"email": "test-profile@example.com", "password": "Password123!"},
        )
        assert login_resp.status_code == 200
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # GET /api/v1/users/me authenticated
        get_resp = await client.get("/api/v1/users/me", headers=headers)
        assert get_resp.status_code == 200
        data = get_resp.json()
        assert data["name"] == "Profile User"
        assert data["email"] == "test-profile@example.com"
        assert data["profile_status"] == "complete"

        # GET /api/v1/users/me unauthenticated -> 401
        unauth_resp = await client.get("/api/v1/users/me")
        assert unauth_resp.status_code == 401

        # PUT /api/v1/users/me update profile
        put_resp = await client.put(
            "/api/v1/users/me",
            json={"name": "Updated Profile User", "phone": "1112223333"},
            headers=headers,
        )
        assert put_resp.status_code == 200
        updated_data = put_resp.json()
        assert updated_data["name"] == "Updated Profile User"
        assert updated_data["phone"] == "1112223333"

    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM users WHERE email = 'test-profile@example.com';"))
        await session.commit()
