from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict


class DocumentBase(BaseModel):
    document_type: str = "Uploaded Document"
    requirement: str = "REQUIRED"


class DocumentCreate(DocumentBase):
    pass


class DocumentResponse(BaseModel):
    id: int
    document_id: str
    owner_id: int
    original_filename: str
    mime_type: str
    file_size: int
    document_type: str
    requirement: str
    status: str
    ocr_status: str
    ai_analysis: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
