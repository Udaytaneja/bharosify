import os
import pytest

from ai.app.core.config import ai_settings
from ai.app.models.model_lifecycle import model_registry_manager
from ai.app.rag import (
    AuthorizationAwareRetriever,
    ChunkAuthorizationMetadata,
    DocumentChunk,
    FileVectorStore,
    PgVectorStore,
    RAGQueryRequest,
    RAGResponse,
    SentenceTransformersEmbeddingProvider,
    pg_vector_store,
    rag_audit_logger,
    secure_rag_pipeline,
    sentence_transformers_embedding_provider,
    vector_store_indexer,
)



@pytest.fixture(autouse=True)
def setup_vector_store():
    """Clears and seeds the vector store before each test."""
    from ai.app.rag.vector_store import file_vector_store
    vector_store_indexer.set_store(file_vector_store)
    vector_store_indexer.clear()



def test_1_real_embedding_provider_interface():
    provider = SentenceTransformersEmbeddingProvider()
    assert provider.model_name == "SentenceTransformers-Embedding"
    assert provider.dimension == 384


def test_2_embedding_dimensions_and_fixture_override():
    provider = SentenceTransformersEmbeddingProvider()
    mock_384_vec = [0.01 * i for i in range(384)]

    vec, meta = provider.embed_text("Test query text", mock_override_vector=mock_384_vec)
    assert len(vec) == 384
    assert meta["dimension"] == 384
    assert meta["status"] == "SUCCESS"


def test_3_unavailable_embedding_model_status():
    provider = SentenceTransformersEmbeddingProvider()
    # Force _get_or_load_st to return unavailable
    provider._get_or_load_st = lambda: (None, False, "SentenceTransformers library is not installed.")

    vec, meta = provider.embed_text("Sample query")
    assert len(vec) == 0
    assert meta["status"] == "MODEL_UNAVAILABLE"
    assert meta["is_available"] is False


def test_4_vector_store_persistence(tmp_path):
    temp_file = str(tmp_path / "test_chunks.json")
    store1 = FileVectorStore(persistence_file=temp_file)

    chunk = DocumentChunk(
        chunk_id="chk_persist_01",
        text="Persistent Document Content",
        embedding=[0.1] * 384,
        metadata=ChunkAuthorizationMetadata(
            document_id="doc_persist",
            document_type="bank_policy",
            organization_id="org_A",
        ),
    )
    store1.upsert([chunk])

    # Re-instantiate store to verify persistence loading across process restarts
    store2 = FileVectorStore(persistence_file=temp_file)
    results = store2.search(query_embedding=[0.1] * 384, query_text="Persistent", organization_id="org_A")
    assert len(results) == 1
    assert results[0][0].chunk_id == "chk_persist_01"



def test_5_document_indexing():
    chunks = secure_rag_pipeline.ingest_document(
        text_content="Standard Banking Operations Policy",
        auth_metadata=ChunkAuthorizationMetadata(
            document_id="doc_idx_01",
            document_type="bank_policy",
            organization_id="org_A",
        ),
    )
    assert len(chunks) >= 1
    assert chunks[0].metadata.organization_id == "org_A"


def test_6_document_deletion_propagation():
    secure_rag_pipeline.ingest_document(
        text_content="Document to be deleted",
        auth_metadata=ChunkAuthorizationMetadata(
            document_id="doc_del_99",
            document_type="bank_policy",
            organization_id="org_A",
        ),
    )

    # Verify present before deletion
    req = RAGQueryRequest(query_text="deleted", organization_id="org_A")
    res1 = secure_rag_pipeline.query(req)
    assert any(c.document_id == "doc_del_99" for c in res1.citations)

    # Perform deletion propagation
    deleted_count = secure_rag_pipeline.delete_document("doc_del_99", "org_A")
    assert deleted_count >= 1

    # Verify no longer retrieved
    res2 = secure_rag_pipeline.query(req)
    assert not any(c.document_id == "doc_del_99" for c in res2.citations)


def test_7_organization_isolation():
    secure_rag_pipeline.ingest_document(
        text_content="Tenant Alpha Confidential Document",
        auth_metadata=ChunkAuthorizationMetadata(
            document_id="doc_alpha",
            document_type="bank_policy",
            organization_id="org_Alpha",
        ),
    )

    req = RAGQueryRequest(query_text="Confidential", organization_id="org_Beta")
    res = secure_rag_pipeline.query(req)
    assert not any(c.document_id == "doc_alpha" for c in res.citations)


def test_8_critical_security_org_a_user_never_receives_org_b_document_context():
    """CRITICAL SECURITY TEST: Org A query MUST NEVER retrieve or send Org B document text to LLM context."""
    # Ingest Org A document
    secure_rag_pipeline.ingest_document(
        text_content="Bank A Confidential Policy: Loan cap is $50,000.",
        auth_metadata=ChunkAuthorizationMetadata(
            document_id="doc_bank_A",
            document_type="bank_policy",
            organization_id="org_A",
        ),
    )

    # Ingest Org B document
    secure_rag_pipeline.ingest_document(
        text_content="Bank B Confidential Policy: Secret vault code is 998877.",
        auth_metadata=ChunkAuthorizationMetadata(
            document_id="doc_bank_B",
            document_type="bank_policy",
            organization_id="org_B",
        ),
    )

    # Execute query as Org A user searching for Secret vault code
    req = RAGQueryRequest(
        query_text="Secret vault code policy",
        organization_id="org_A",
        user_id=101,
        role="user",
    )

    res = secure_rag_pipeline.query(req)

    # Verify Org B document is NOT in citations
    for citation in res.citations:
        assert citation.document_id != "doc_bank_B"
        assert "998877" not in citation.snippet

    # Verify Org B document text is NOT in LLM answer
    assert "998877" not in res.answer
    assert "Bank B" not in res.answer


def test_9_role_restrictions_banker_vs_user():
    secure_rag_pipeline.ingest_document(
        text_content="Restricted Banker Guidance",
        auth_metadata=ChunkAuthorizationMetadata(
            document_id="doc_banker_only",
            document_type="governance_policy",
            organization_id="org_A",
            allowed_roles=["banker"],
            data_sensitivity="restricted",
        ),
    )

    user_req = RAGQueryRequest(query_text="Guidance", organization_id="org_A", role="user")
    user_res = secure_rag_pipeline.query(user_req)
    assert not any(c.document_id == "doc_banker_only" for c in user_res.citations)

    banker_req = RAGQueryRequest(query_text="Guidance", organization_id="org_A", role="banker")
    banker_res = secure_rag_pipeline.query(banker_req)
    assert any(c.document_id == "doc_banker_only" for c in banker_res.citations)


def test_10_inactive_document_versions_filtered():
    secure_rag_pipeline.ingest_document(
        text_content="Outdated Version 0.5 Policy",
        auth_metadata=ChunkAuthorizationMetadata(
            document_id="doc_v05",
            document_type="bank_policy",
            organization_id="org_A",
            is_active_version=False,
        ),
    )

    req = RAGQueryRequest(query_text="Outdated", organization_id="org_A")
    res = secure_rag_pipeline.query(req)
    assert not any(c.document_id == "doc_v05" for c in res.citations)


def test_11_insufficient_evidence_status_handling():
    req = RAGQueryRequest(
        query_text="NonExistentTopicRandomStringXYZ99",
        organization_id="org_Empty",
    )

    res = secure_rag_pipeline.query(req)
    assert res.grounding_status == "INSUFFICIENT_EVIDENCE"
    assert res.grounded is False
    assert "INSUFFICIENT_EVIDENCE" in res.answer


def test_12_grounded_response_generation():
    secure_rag_pipeline.ingest_document(
        text_content="Official Standard Repayment Terms: Interest rate is 10.5%.",
        auth_metadata=ChunkAuthorizationMetadata(
            document_id="doc_repay",
            document_type="bank_policy",
            organization_id="org_A",
        ),
    )

    req = RAGQueryRequest(query_text="Repayment Interest rate", organization_id="org_A")
    res = secure_rag_pipeline.query(req)

    assert res.grounding_status == "GROUNDED"
    assert res.grounded is True
    assert len(res.citations) >= 1
    assert "doc_repay" in res.citations[0].document_id


def test_13_audit_logging_and_pii_redaction():
    req = RAGQueryRequest(
        query_text="Sensitive query containing PAN ABCDE1234F",
        organization_id="org_A",
    )
    secure_rag_pipeline.query(req)

    events = rag_audit_logger.get_events()
    assert len(events) >= 1
    last_event = events[-1]
    assert last_event.organization_id == "org_A"
    assert len(last_event.query_hash) > 0
    # Raw query text is NOT present in audit event (only SHA-256 query hash)
    assert not hasattr(last_event, "query_text")
