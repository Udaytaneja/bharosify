import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Sequence

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.document import Document
from backend.app.models.user import User
from ai.app.perception import document_intelligence_pipeline

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB limit


async def create_user_document(
    db: AsyncSession,
    file: UploadFile,
    owner_id: int,
    document_type: str = "Uploaded Document",
) -> Document:
    original_filename = Path(file.filename or "document.pdf").name
    ext = Path(original_filename).suffix.lower()
    if ext not in {".pdf", ".png", ".jpg", ".jpeg"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Only PDF, PNG, JPG, and JPEG files are supported.",
        )

    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds the 25MB limit.",
        )

    # Secure storage UUID filename
    doc_uuid = str(uuid.uuid4())
    stored_filename = f"{doc_uuid}{ext if ext else '.pdf'}"
    file_path = UPLOAD_DIR / stored_filename

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    # Run AI perception pipeline
    ai_result_dict = None
    status_str = "VERIFIED"
    ocr_status_str = "COMPLETED"

    try:
        pipeline_result = await document_intelligence_pipeline.process_document(
            file_bytes=file_bytes,
            file_name=original_filename,
        )
        if hasattr(pipeline_result, "model_dump"):
            ai_result_dict = pipeline_result.model_dump()
        elif isinstance(pipeline_result, dict):
            ai_result_dict = pipeline_result
        else:
            ai_result_dict = dict(pipeline_result)

        if ai_result_dict and ai_result_dict.get("requires_review"):
            status_str = "PROCESSING_OCR"

        ocr_lines = ai_result_dict.get("ocr_lines", []) if ai_result_dict else []
        if not ocr_lines:
            ocr_status_str = "UNAVAILABLE"
    except Exception as exc:
        print(f"AI perception pipeline warning during document upload: {exc}")
        ocr_status_str = "UNAVAILABLE"

    doc = Document(
        document_id=doc_uuid,
        owner_id=owner_id,
        original_filename=original_filename,
        stored_filename=stored_filename,
        mime_type=file.content_type or "application/pdf",
        file_size=len(file_bytes),
        document_type=document_type,
        requirement="REQUIRED",
        status=status_str,
        ocr_status=ocr_status_str,
        ai_analysis=ai_result_dict,
    )

    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc


async def list_user_documents(db: AsyncSession, current_user: User) -> Sequence[Document]:
    if current_user.role == "banker":
        query = select(Document).order_by(Document.created_at.desc())
    else:
        query = (
            select(Document)
            .where(Document.owner_id == current_user.id)
            .order_by(Document.created_at.desc())
        )
    result = await db.execute(query)
    return result.scalars().all()


async def get_document_by_id(
    db: AsyncSession, document_id: str, current_user: User
) -> Document | None:
    query = select(Document).where(Document.document_id == document_id)
    result = await db.execute(query)
    doc = result.scalar_one_or_none()

    if doc is None:
        return None

    if current_user.role != "banker" and doc.owner_id != current_user.id:
        return None

    return doc


async def get_document_file_path(
    db: AsyncSession, document_id: str, current_user: User
) -> tuple[Path, str, str] | None:
    doc = await get_document_by_id(db, document_id, current_user)
    if doc is None:
        return None

    file_path = UPLOAD_DIR / doc.stored_filename
    if not file_path.exists():
        return None

    return file_path, doc.original_filename, doc.mime_type
