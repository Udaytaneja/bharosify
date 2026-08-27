from typing import Dict, Any, List
from pydantic import BaseModel, Field
from ai.app.perception.tampering import DocumentAnomaly


class DocumentIntelligenceResult(BaseModel):
    """Contract response schema required for Document Intelligence."""
    document_type: str  # "identity_document" | "bank_statement" | "salary_slip" | "loan_document" | "financial_form"
    fields: Dict[str, Any]
    confidence: float = Field(ge=0.0, le=1.0)
    anomalies: List[Dict[str, Any]] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)
    model_metadata: Dict[str, Any] = Field(default_factory=dict)
    layout_regions: List[Dict[str, Any]] = Field(default_factory=list)
    ocr_lines: List[Dict[str, Any]] = Field(default_factory=list)
    requires_review: bool


class DocumentBackendAdapter:
    """Transforms raw pipeline stages into standard DocumentIntelligenceResult."""

    def format_result(
        self,
        document_type: str,
        fields: Dict[str, Any],
        confidence: float,
        anomalies: List[DocumentAnomaly],
        evidence: List[str],
        model_metadata: Dict[str, Any],
        layout_regions: List[Dict[str, Any]],
        ocr_lines: List[Dict[str, Any]],
        requires_review: bool,
    ) -> DocumentIntelligenceResult:
        formatted_anomalies = [a.model_dump() for a in anomalies]

        return DocumentIntelligenceResult(
            document_type=document_type,
            fields=fields,
            confidence=confidence,
            anomalies=formatted_anomalies,
            evidence=evidence,
            model_metadata=model_metadata,
            layout_regions=layout_regions,
            ocr_lines=ocr_lines,
            requires_review=requires_review,
        )


document_backend_adapter = DocumentBackendAdapter()
