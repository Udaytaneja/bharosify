import hashlib
import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RAGAuditEvent(BaseModel):
    """Audit log entry for RAG query and retrieval operations."""

    request_id: str
    organization_id: str
    user_id: Optional[int] = None
    query_hash: str  # SHA-256 hash of query_text for PII protection
    retrieved_document_ids: List[str] = Field(default_factory=list)
    retrieved_chunk_ids: List[str] = Field(default_factory=list)
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    latency_ms: float = 0.0
    result_status: str = "GROUNDED"  # "GROUNDED" | "PARTIALLY_GROUNDED" | "INSUFFICIENT_EVIDENCE"
    timestamp: str = Field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()))


class RAGAuditLogger:
    """
    RAG Audit Logger recording query hashes, chunk IDs, and latency metrics
    while redacting sensitive PII document contents.
    """

    def __init__(self):
        self._audit_events: List[RAGAuditEvent] = []

    def log_event(
        self,
        request_id: str,
        organization_id: str,
        user_id: Optional[int],
        query_text: str,
        retrieved_document_ids: List[str],
        retrieved_chunk_ids: List[str],
        embedding_model: str,
        latency_ms: float,
        result_status: str,
    ) -> RAGAuditEvent:
        """Logs a redacted audit event."""
        query_hash = hashlib.sha256(query_text.encode("utf-8")).hexdigest()[:16]

        event = RAGAuditEvent(
            request_id=request_id,
            organization_id=organization_id,
            user_id=user_id,
            query_hash=query_hash,
            retrieved_document_ids=retrieved_document_ids,
            retrieved_chunk_ids=retrieved_chunk_ids,
            embedding_model=embedding_model,
            latency_ms=round(latency_ms, 2),
            result_status=result_status,
        )

        self._audit_events.append(event)
        return event

    def get_events(self) -> List[RAGAuditEvent]:
        return list(self._audit_events)


rag_audit_logger = RAGAuditLogger()
