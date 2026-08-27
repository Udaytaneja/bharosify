# AI RAG PostgreSQL Database Schema Specification - AgentTrust OS

**Author**: Member 3 (AI/ML/LLM/Agent Intelligence Subsystem Lead)  
**Date**: August 25, 2026  
**Scope**: `document_chunks` table and vector index specification

---

## Database Table Specification: `document_chunks`

```sql
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
```

---

## Vector Similarity Query Specification

```sql
SELECT
    chunk_id, document_id, organization_id, chunk_text, document_type,
    policy_version, is_active, is_deleted, user_id, allowed_roles,
    data_sensitivity, consent_given,
    1 - (embedding <=> %s::vector) AS similarity
FROM document_chunks
WHERE organization_id = %s
  AND is_active = TRUE
  AND is_deleted = FALSE
ORDER BY embedding <=> %s::vector ASC
LIMIT %s;
```
