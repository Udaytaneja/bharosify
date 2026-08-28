import io
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import engine
from backend.app.main import app
from backend.app.models.user import User
from backend.app.services.auth_service import create_auth_tokens


@pytest.mark.asyncio
async def test_document_upload_persistence_and_isolation():
    async with AsyncSession(engine) as session:
        # 1. Create User 1 (Applicant)
        user1 = User(
            name="Applicant One",
            email="applicant1@agenttrust.com",
            hashed_password="hashed_pass_123",
            role="user",
            is_active=True,
            is_verified=True,
        )
        session.add(user1)

        # 2. Create User 2 (Applicant 2)
        user2 = User(
            name="Applicant Two",
            email="applicant2@agenttrust.com",
            hashed_password="hashed_pass_123",
            role="user",
            is_active=True,
            is_verified=True,
        )
        session.add(user2)
        await session.commit()
        await session.refresh(user1)
        await session.refresh(user2)

        tokens1 = create_auth_tokens(user1)
        headers1 = {"Authorization": f"Bearer {tokens1['access_token']}"}

        tokens2 = create_auth_tokens(user2)
        headers2 = {"Authorization": f"Bearer {tokens2['access_token']}"}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 3. User 1 Uploads Document
        file_content = b"%PDF-1.4 mock tax return content for testing persistence"
        files = {"file": ("Tax_Return_2023.pdf", io.BytesIO(file_content), "application/pdf")}
        data = {"document_type": "Tax Return"}

        upload_res = await client.post(
            "/api/v1/documents/upload", headers=headers1, files=files, data=data
        )
        assert upload_res.status_code == 201, upload_res.text
        doc_data = upload_res.json()
        assert doc_data["original_filename"] == "Tax_Return_2023.pdf"
        assert doc_data["document_type"] == "Tax Return"
        doc_id = doc_data["document_id"]

        # 4. User 1 Lists Documents -> Document exists
        list_res1 = await client.get("/api/v1/documents", headers=headers1)
        assert list_res1.status_code == 200
        docs1 = list_res1.json()
        assert len(docs1) == 1
        assert docs1[0]["document_id"] == doc_id

        # 5. User 2 Lists Documents -> Isolated, User 2 gets 0 documents
        list_res2 = await client.get("/api/v1/documents", headers=headers2)
        assert list_res2.status_code == 200
        docs2 = list_res2.json()
        assert len(docs2) == 0

        # 6. User 2 tries to download User 1's document -> 404/Unauthorized
        download_res2 = await client.get(f"/api/v1/documents/{doc_id}/download", headers=headers2)
        assert download_res2.status_code in {404, 403}

        # 7. User 1 downloads own document -> 200 OK
        download_res1 = await client.get(f"/api/v1/documents/{doc_id}/download", headers=headers1)
        assert download_res1.status_code == 200
        assert download_res1.content == file_content
