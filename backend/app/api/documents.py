from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.document import DocumentResponse
from backend.app.services.document_service import (
    create_user_document,
    get_document_by_id,
    get_document_file_path,
    list_user_documents,
)

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = Form("Uploaded Document"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Upload and persist a document for current authenticated user with AI perception analysis."""
    return await create_user_document(
        db=db, file=file, owner_id=current_user.id, document_type=document_type
    )


@router.get("", response_model=list[DocumentResponse])
async def get_documents(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """List documents owned by current authenticated user (or all documents if banker)."""
    return await list_user_documents(db=db, current_user=current_user)


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get metadata for a specific document by document_id."""
    doc = await get_document_by_id(db=db, document_id=document_id, current_user=current_user)
    if doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found or unauthorized",
        )
    return doc


@router.get("/{document_id}/download")
async def download_document(
    document_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Securely download file content for authorized owner or banker."""
    res = await get_document_file_path(db=db, document_id=document_id, current_user=current_user)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document file not found or unauthorized",
        )
    file_path, filename, media_type = res
    return FileResponse(path=file_path, filename=filename, media_type=media_type)
