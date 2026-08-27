import os
import pytest

from ai.app.core.config import ai_settings
from ai.app.rag import (
    ChunkAuthorizationMetadata,
    DocumentChunk,
    PgVectorStore,
    RAGQueryRequest,
    secure_rag_pipeline,
    vector_store_indexer,
)

# Check if a live PostgreSQL instance is configured
HAS_POSTGRES = bool(ai_settings.pgvector_host or ai_settings.pgvector_url)


@pytest.mark.skipif(
    not HAS_POSTGRES,
    reason="INTEGRATION TESTS: BLOCKED — POSTGRESQL/PGVECTOR NOT AVAILABLE (PGVECTOR_HOST is unconfigured)"
)
def test_pgvector_integration_connection_and_extension():
    """Live Integration Test 1: Verify PostgreSQL connection & pgvector extension."""
    pg_store = PgVectorStore()
    health = pg_store.health()
    assert health["status"] == "HEALTHY"


@pytest.mark.skipif(
    not HAS_POSTGRES,
    reason="INTEGRATION TESTS: BLOCKED — POSTGRESQL/PGVECTOR NOT AVAILABLE (PGVECTOR_HOST is unconfigured)"
)
def test_pgvector_integration_vector_insertion_and_search():
    """Live Integration Test 2: Real PostgreSQL vector insertion and pgvector SQL search."""
    pg_store = PgVectorStore()

    chunk = DocumentChunk(
        chunk_id="chk_pg_int_01",
        text="Live PostgreSQL pgvector Integration Test Content",
        embedding=[0.05] * 384,
        metadata=ChunkAuthorizationMetadata(
            document_id="doc_pg_int_01",
            document_type="bank_policy",
            organization_id="org_pg_test",
        ),
    )

    pg_store.upsert([chunk])

    results = pg_store.search(
        query_embedding=[0.05] * 384,
        query_text="Integration Test",
        organization_id="org_pg_test",
        top_k=5,
    )

    assert len(results) >= 1
    assert results[0][0].chunk_id == "chk_pg_int_01"


@pytest.mark.skipif(
    not HAS_POSTGRES,
    reason="INTEGRATION TESTS: BLOCKED — POSTGRESQL/PGVECTOR NOT AVAILABLE (PGVECTOR_HOST is unconfigured)"
)
def test_pgvector_integration_tenant_isolation():
    """Live Integration Test 3: SQL level organization_id tenant isolation."""
    pg_store = PgVectorStore()

    chunk_A = DocumentChunk(
        chunk_id="chk_pg_org_A",
        text="Org A Confidential Data in Postgres",
        embedding=[0.02] * 384,
        metadata=ChunkAuthorizationMetadata(
            document_id="doc_pg_org_A",
            document_type="bank_policy",
            organization_id="org_A_live",
        ),
    )

    chunk_B = DocumentChunk(
        chunk_id="chk_pg_org_B",
        text="Org B Confidential Data in Postgres",
        embedding=[0.02] * 384,
        metadata=ChunkAuthorizationMetadata(
            document_id="doc_pg_org_B",
            document_type="bank_policy",
            organization_id="org_B_live",
        ),
    )

    pg_store.upsert([chunk_A, chunk_B])

    results_A = pg_store.search(
        query_embedding=[0.02] * 384,
        query_text="Confidential Data",
        organization_id="org_A_live",
    )

    assert all(r[0].metadata.organization_id == "org_A_live" for r in results_A)
    assert not any(r[0].chunk_id == "chk_pg_org_B" for r in results_A)
