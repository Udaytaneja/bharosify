# PostgreSQL + pgvector RAG Infrastructure Setup - AgentTrust OS

**Author**: Member 3 (AI/ML/LLM/Agent Intelligence Subsystem Lead)  
**Date**: August 25, 2026  
**Scope**: Production PostgreSQL + pgvector Activation & Migration Guide

---

## 1. Prerequisites & PostgreSQL Configuration

### Minimum Requirements
- **PostgreSQL Version**: 15.0 or higher
- **PostgreSQL Extension**: `pgvector` (`v0.5.0`+)
- **Python Driver**: `psycopg2-binary` or `asyncpg`

### Environment Variables
Configure in `.env`:
```ini
PGVECTOR_HOST=localhost
PGVECTOR_PORT=5432
PGVECTOR_DATABASE=agenttrust_ai
PGVECTOR_USER=postgres
PGVECTOR_PASSWORD=your_secure_password_here
# Optional full DSN override:
# PGVECTOR_URL=postgresql://postgres:your_secure_password_here@localhost:5432/agenttrust_ai
```

---

## 2. Database Migration Execution

Execute migration script [`contracts/sql/rag_vector_schema.sql`](file:///d:/Agenttrust-os-/contracts/sql/rag_vector_schema.sql):

```bash
psql -h localhost -U postgres -d agenttrust_ai -f contracts/sql/rag_vector_schema.sql
```

---

## 3. Production Behavior & Zero JSON Fallback Guarantee

- **Authoritative Database**: [`PgVectorStore`](file:///d:/Agenttrust-os-/ai/app/rag/vector_store.py) is the sole production vector store.
- **No Production JSON Fallback**: If PostgreSQL or `pgvector` extension is unconfigured/offline, operations fail fast returning `PGVECTOR_REQUIRED` or `DATABASE_UNAVAILABLE`. Production RAG does **NOT** silently fall back to `data/vector_store_chunks.json`.
- **Isolated Test Store**: [`FileVectorStore`](file:///d:/Agenttrust-os-/ai/app/rag/vector_store.py) is isolated strictly for offline unit tests (`ai/tests/test_rag_unit.py`).
