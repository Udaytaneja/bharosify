import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from backend.app.core.database import AsyncSessionLocal
from backend.app.main import app


@pytest.mark.asyncio
async def test_register_and_login_flow():
    # Clean up test user if exists
    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM users WHERE email = 'test-pytest@example.com';"))
        await session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Test registration
        reg_payload = {
            "name": "Pytest User",
            "email": "test-pytest@example.com",
            "password": "TestPassword123!",
            "phone": "9876543210",
            "language": "en",
        }
        res_reg = await client.post("/api/v1/auth/register", json=reg_payload)
        assert res_reg.status_code == 201
        data = res_reg.json()
        assert data["name"] == "Pytest User"
        assert data["email"] == "test-pytest@example.com"
        assert data["phone"] == "9876543210"
        assert data["role"] == "user"
        assert data["language"] == "en"

        # Test login
        login_payload = {
            "email": "test-pytest@example.com",
            "password": "TestPassword123!",
        }
        res_login = await client.post("/api/v1/auth/login", json=login_payload)
        assert res_login.status_code == 200
        token_data = res_login.json()
        assert "access_token" in token_data
        assert "refresh_token" in token_data
        assert token_data["token_type"] == "bearer"
        assert token_data["user"]["email"] == "test-pytest@example.com"

    # Clean up after test
    async with AsyncSessionLocal() as session:
        await session.execute(text("DELETE FROM users WHERE email = 'test-pytest@example.com';"))
        await session.commit()
