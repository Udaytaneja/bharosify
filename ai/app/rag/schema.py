from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ChunkAuthorizationMetadata(BaseModel):
    """Mandatory Authorization & Access Control Metadata bound to EVERY chunk."""
    document_id: str
    document_type: str  # "bank_policy" | "product_rule" | "governance_policy" | "agent_policy" | "compliance" | "financial_document"
    organization_id: str
    user_id: Optional[int] = None
    allowed_roles: List[str] = Field(default_factory=lambda: ["user", "banker"])
    data_sensitivity: str = "internal"  # "public" | "internal" | "confidential" | "restricted"
    consent_given: bool = True
    is_deleted: bool = False
    policy_version: str = "1.0.0"
    is_active_version: bool = True
    effective_until: Optional[str] = None


class DocumentChunk(BaseModel):
    """Document Chunk holding text, vector embedding, and authorization metadata."""
    chunk_id: str
    text: str
    embedding: List[float] = Field(default_factory=list)
    metadata: ChunkAuthorizationMetadata


class RAGQueryRequest(BaseModel):
    """Permission-aware retrieval request context."""
    query_text: str
    organization_id: str
    user_id: Optional[int] = None
    role: str = "user"  # "user" | "banker"
    language: str = "en"
    top_k: int = 5


class Citation(BaseModel):
    document_id: str
    document_type: str
    policy_version: str
    snippet: str
    relevance_score: float


class RAGResponse(BaseModel):
    answer: str
    citations: List[Citation] = Field(default_factory=list)
    chunks_retrieved_count: int
    chunks_filtered_count: int
    prompt_injection_detected: bool = False
    grounded: bool = True
    grounding_status: str = "GROUNDED"  # "GROUNDED" | "PARTIALLY_GROUNDED" | "INSUFFICIENT_EVIDENCE"
    requires_human_review: bool = False
    model_metadata: Dict[str, Any] = Field(default_factory=dict)

