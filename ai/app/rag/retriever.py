from typing import List, Tuple
from ai.app.rag.embedding import sentence_transformers_embedding_provider
from ai.app.rag.indexer import vector_store_indexer
from ai.app.rag.schema import DocumentChunk, RAGQueryRequest


class PermissionAwareRetriever:
    """
    AuthorizationAwareRetriever enforcing Pre-LLM Security Filters:
    1. Multi-tenant isolation (organization_id WHERE clause)
    2. Non-deletion status (is_deleted == False)
    3. Active policy versioning (is_active_version == True)
    4. Consent status (consent_given == True)
    5. Role-based access control (role in allowed_roles)
    6. Data sensitivity limits (restricted docs require banker role)
    7. User isolation (user_id scoping)
    CRITICAL RULE: Unauthorized context MUST NEVER reach the LLM.
    """

    def retrieve(self, request: RAGQueryRequest) -> Tuple[List[Tuple[DocumentChunk, float]], int]:
        """
        Executes permission-aware retrieval.
        Returns:
            Tuple[retrieved_authorized_chunks_with_scores, filtered_count]
        """
        # Generate real 384d embedding vector for query
        query_vec, embed_meta = sentence_transformers_embedding_provider.embed_text(request.query_text)

        # Vector Store query with HARD TENANT ISOLATION (WHERE organization_id = %s)
        raw_candidates = vector_store_indexer.search_raw(
            query_text=request.query_text,
            organization_id=request.organization_id,
            query_embedding=query_vec,
            top_k=request.top_k * 5,
        )

        authorized_chunks: List[Tuple[DocumentChunk, float]] = []
        filtered_count = 0

        for chunk, score in raw_candidates:
            meta = chunk.metadata

            # 1. PREVENT CROSS-TENANT ACCESS: organization_id MUST match
            if meta.organization_id != request.organization_id:
                filtered_count += 1
                continue

            # 2. FILTER DELETED DOCUMENTS: is_deleted MUST be False
            if meta.is_deleted:
                filtered_count += 1
                continue

            # 3. FILTER OUTDATED POLICY VERSIONS: is_active_version MUST be True
            if not meta.is_active_version:
                filtered_count += 1
                continue

            # 4. FILTER CONSENT REVOKED DATA: consent_given MUST be True
            if not meta.consent_given:
                filtered_count += 1
                continue

            # 5. ROLE ACCESS CONTROL: request.role MUST be in allowed_roles
            if request.role not in meta.allowed_roles:
                filtered_count += 1
                continue

            # 6. SENSITIVITY PRIVILEGE CONTROL: Restricted data requires banker role
            if meta.data_sensitivity == "restricted" and request.role != "banker":
                filtered_count += 1
                continue

            # 7. USER ISOLATION FOR PRIVATE FINANCIAL DOCUMENTS:
            if meta.user_id is not None:
                if request.role == "user" and meta.user_id != request.user_id:
                    filtered_count += 1
                    continue

            authorized_chunks.append((chunk, score))
            if len(authorized_chunks) >= request.top_k:
                break

        return authorized_chunks, filtered_count


# Alias for explicit Phase 2C architecture naming
AuthorizationAwareRetriever = PermissionAwareRetriever
permission_aware_retriever = PermissionAwareRetriever()
