import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from backend.app.core.database import AsyncSessionLocal
from backend.app.main import app


@pytest.mark.asyncio
async def test_authentication_hardening_flow():
    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM users WHERE email = 'test-hardened@example.com';"))
        await session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Register user
        reg_resp = await client.post(
            "/api/v1/auth/register",
            json={
                "name": "Hardened User",
                "email": "test-hardened@example.com",
                "password": "Password123!",
                "phone": "1234567890",
                "language": "en",
            },
        )
        assert reg_resp.status_code == 201

        # 2. Login user
        login_resp = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "test-hardened@example.com",
                "password": "Password123!",
            },
        )
        assert login_resp.status_code == 200
        tokens = login_resp.json()
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]

        # 3. GET /api/v1/auth/me authenticated
        me_resp = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert me_resp.status_code == 200
        user_data = me_resp.json()
        assert user_data["email"] == "test-hardened@example.com"
        assert user_data["name"] == "Hardened User"

        # 4. GET /api/v1/auth/me unauthenticated
        unauth_resp = await client.get("/api/v1/auth/me")
        assert unauth_resp.status_code == 401

        # 5. POST /api/v1/auth/refresh
        ref_resp = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        assert ref_resp.status_code == 200
        new_tokens = ref_resp.json()
        assert "access_token" in new_tokens
        assert "refresh_token" in new_tokens

        # 6. Logout / token revocation
        logout_resp = await client.post(
            "/api/v1/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert logout_resp.status_code == 200

        # 7. Accessing me with revoked token fails
        revoked_resp = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert revoked_resp.status_code == 401

    # Cleanup
    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM users WHERE email = 'test-hardened@example.com';"))
        await session.commit()
