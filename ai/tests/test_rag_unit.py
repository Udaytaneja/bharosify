import pytest

from ai.app.rag import (
    AuthorizationAwareRetriever,
    ChunkAuthorizationMetadata,
    DocumentChunk,
    PgVectorStore,
    RAGQueryRequest,
    RAGResponse,
    SentenceTransformersEmbeddingProvider,
    file_vector_store,
    rag_audit_logger,
    secure_rag_pipeline,
    vector_store_indexer,
)


@pytest.fixture(autouse=True)
def setup_unit_test_vector_store():
    """Sets offline FileVectorStore for fast unit tests without PostgreSQL requirement."""
    vector_store_indexer.set_store(file_vector_store)
    vector_store_indexer.clear()


def test_unit_1_pgvector_store_health_reports_unconfigured_when_no_host():
    """Verify PgVectorStore.health() reports CONFIGURATION_MISSING or DATABASE_UNAVAILABLE when host is empty."""
    pg_store = PgVectorStore()
    health = pg_store.health()
    assert health["status"] in ("CONFIGURATION_MISSING", "DATABASE_UNAVAILABLE")


def test_unit_2_pgvector_store_fails_fast_without_db_connection():
    """Verify PgVectorStore.upsert() fails fast with PGVECTOR_REQUIRED without silently creating JSON files."""
    pg_store = PgVectorStore()
    chunk = DocumentChunk(
        chunk_id="chk_unit_fail",
        text="Unit Test Content",
        embedding=[0.1] * 384,
        metadata=ChunkAuthorizationMetadata(
            document_id="doc_unit",
            document_type="bank_policy",
            organization_id="org_A",
        ),
    )

    with pytest.raises(RuntimeError, match="PGVECTOR_REQUIRED"):
        pg_store.upsert([chunk])


def test_unit_3_pre_llm_authorization_filtering():
    """Verify pre-LLM AuthorizationAwareRetriever filters unauthorized chunks in unit mode."""
    secure_rag_pipeline.ingest_document(
        text_content="Org A Private Document",
        auth_metadata=ChunkAuthorizationMetadata(
            document_id="doc_org_A_private",
            document_type="financial_document",
            organization_id="org_A",
            user_id=101,
        ),
    )

    req = RAGQueryRequest(query_text="Private Document", organization_id="org_A", user_id=102)
    res = secure_rag_pipeline.query(req)
    assert not any(c.document_id == "doc_org_A_private" for c in res.citations)


def test_unit_4_critical_security_org_a_user_never_receives_org_b_context():
    """CRITICAL SECURITY UNIT TEST: Org A query MUST NEVER retrieve Org B document context."""
    secure_rag_pipeline.ingest_document(
        text_content="Bank A Policy: Maximum loan $50,000.",
        auth_metadata=ChunkAuthorizationMetadata(
            document_id="doc_bank_A",
            document_type="bank_policy",
            organization_id="org_A",
        ),
    )

    secure_rag_pipeline.ingest_document(
        text_content="Bank B Policy: Secret vault code is 998877.",
        auth_metadata=ChunkAuthorizationMetadata(
            document_id="doc_bank_B",
            document_type="bank_policy",
            organization_id="org_B",
        ),
    )

    req = RAGQueryRequest(query_text="Secret vault code policy", organization_id="org_A")
    res = secure_rag_pipeline.query(req)

    for citation in res.citations:
        assert citation.document_id != "doc_bank_B"
        assert "998877" not in citation.snippet

    assert "998877" not in res.answer
    assert "Bank B" not in res.answer


def test_unit_5_role_restrictions_user_vs_banker():
    secure_rag_pipeline.ingest_document(
        text_content="Restricted Banker Protocol Code RED",
        auth_metadata=ChunkAuthorizationMetadata(
            document_id="doc_banker_restricted",
            document_type="governance_policy",
            organization_id="org_A",
            allowed_roles=["banker"],
            data_sensitivity="restricted",
        ),
    )

    user_req = RAGQueryRequest(query_text="Protocol Code RED", organization_id="org_A", role="user")
    user_res = secure_rag_pipeline.query(user_req)
    assert not any(c.document_id == "doc_banker_restricted" for c in user_res.citations)

    banker_req = RAGQueryRequest(query_text="Protocol Code RED", organization_id="org_A", role="banker")
    banker_res = secure_rag_pipeline.query(banker_req)
    assert any(c.document_id == "doc_banker_restricted" for c in banker_res.citations)


def test_unit_6_document_versioning_only_active_version_retrieved():
    """Verify v1 active, v2 active, v1 inactive -> Query only returns v2 active version."""
    secure_rag_pipeline.ingest_document(
        text_content="Policy Version 1 (Inactive)",
        auth_metadata=ChunkAuthorizationMetadata(
            document_id="doc_v1",
            document_type="bank_policy",
            organization_id="org_A",
            policy_version="1.0.0",
            is_active_version=False,  # INACTIVE
        ),
    )

    secure_rag_pipeline.ingest_document(
        text_content="Policy Version 2 (Active Current)",
        auth_metadata=ChunkAuthorizationMetadata(
            document_id="doc_v2",
            document_type="bank_policy",
            organization_id="org_A",
            policy_version="2.0.0",
            is_active_version=True,  # ACTIVE
        ),
    )

    req = RAGQueryRequest(query_text="Policy Version", organization_id="org_A")
    res = secure_rag_pipeline.query(req)

    for citation in res.citations:
        assert citation.document_id != "doc_v1"
    assert any(c.document_id == "doc_v2" for c in res.citations)
