-- ============================================================================
-- AgentTrust OS RAG Subsystem Migration 001: PostgreSQL + pgvector Schema
-- Extension: vector
-- Table: document_chunks
-- ============================================================================

-- 1. Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Document Chunks Table with vector(384) column
CREATE TABLE IF NOT EXISTS document_chunks (
    chunk_id VARCHAR(128) PRIMARY KEY,
    document_id VARCHAR(128) NOT NULL,
    organization_id VARCHAR(128) NOT NULL,
    owner_id VARCHAR(128),
    chunk_text TEXT NOT NULL,
    embedding vector(384),
    embedding_model VARCHAR(128) DEFAULT 'sentence-transformers/all-MiniLM-L6-v2',
    embedding_version VARCHAR(32) DEFAULT 'v1.0.0',
    document_type VARCHAR(64) NOT NULL,
    classification VARCHAR(64) DEFAULT 'internal',
    page_number INTEGER DEFAULT 1,
    document_version VARCHAR(32) DEFAULT '1.0.0',
    is_active BOOLEAN DEFAULT TRUE,
    is_deleted BOOLEAN DEFAULT FALSE,
    user_id INTEGER,
    allowed_roles JSONB DEFAULT '["user", "banker"]'::jsonb,
    data_sensitivity VARCHAR(32) DEFAULT 'internal',
    consent_given BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- 3. Composite Indexes for Hard Multi-Tenant Isolation & Active State Queries
CREATE INDEX IF NOT EXISTS idx_chunks_org_id ON document_chunks(organization_id);
CREATE INDEX IF NOT EXISTS idx_chunks_doc_id ON document_chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_chunks_active_deleted ON document_chunks(organization_id, is_active, is_deleted);

-- Optional HNSW Vector Cosine Distance Index for large datasets
-- CREATE INDEX IF NOT EXISTS idx_chunks_vec_hnsw ON document_chunks USING hnsw (embedding vector_cosine_ops);
