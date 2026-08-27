from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from ai.app.rag import RAGQueryRequest, RAGResponse, secure_rag_pipeline


class AssistantRAGAdapter:
    """
    RAG Adapter for Financial Intelligence Assistant.
    Retrieves authorized policy documents and citations safely.
    Returns INSUFFICIENT_EVIDENCE when policy documents are absent.
    """

    def query_policy(
        self,
        query_text: str,
        organization_id: str,
        user_id: Optional[int] = None,
        role: str = "user",
    ) -> RAGResponse:
        req = RAGQueryRequest(
            query_text=query_text,
            organization_id=organization_id,
            user_id=user_id,
            role=role,
            top_k=3,
        )
        return secure_rag_pipeline.query(req)


assistant_rag_adapter = AssistantRAGAdapter()
