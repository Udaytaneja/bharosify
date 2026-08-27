from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DocumentIntelligenceDTO(BaseModel):
    """Canonical contract DTO for Document Perception results."""
    document_id: str = Field(description="Document identifier")
    organization_id: Optional[str] = Field(default=None, description="Multi-tenant organization boundary")
    document_type: str = Field(description="Document category e.g. bank_statement, salary_slip, pan_card")
    extracted_fields: Dict[str, Any] = Field(default_factory=dict, description="Extracted key-value pairs")
    confidence: float = Field(ge=0.0, le=1.0, description="Overall perception confidence score")
    detected_elements: List[Dict[str, Any]] = Field(default_factory=list, description="Layout bounding boxes and structural elements")
    validation_status: str = Field(default="valid", description="Validation status e.g. valid, invalid, warning")
    tampering_status: str = Field(default="clean", description="Tampering analysis status e.g. clean, tampered, suspicious")
