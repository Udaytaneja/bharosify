import pytest
from httpx import ASGITransport, AsyncClient

from backend.app.main import app


@pytest.mark.asyncio
async def test_standard_error_response_format():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. 401 Unauthorized Error
        r_unauth = await client.get("/api/v1/auth/me")
        assert r_unauth.status_code == 401
        err_unauth = r_unauth.json()
        assert "error" in err_unauth
        assert err_unauth["error"]["code"] == "UNAUTHORIZED"
        assert "message" in err_unauth["error"]

        # 2. 404 Not Found Error
        r_notfound = await client.get("/api/v1/loans/999999", headers={"Authorization": "Bearer invalid_token"})
        assert r_notfound.status_code in (401, 404)
        err_nf = r_notfound.json()
        assert "error" in err_nf

        # 3. 422 Validation Error
        r_val = await client.post("/api/v1/auth/register", json={"email": "invalid-email"})
        assert r_val.status_code == 422
        err_val = r_val.json()
        assert "error" in err_val
        assert err_val["error"]["code"] == "VALIDATION_ERROR"
        assert err_val["error"]["details"] is not None
