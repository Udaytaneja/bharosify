# AI RAG Operations & Maintenance Guide - AgentTrust OS

**Author**: Member 3 (AI/ML/LLM/Agent Intelligence Subsystem Lead)  
**Date**: August 25, 2026  
**Scope**: Configuration, Operations, Failure Modes & Health Diagnostics

---

## Configuration Reference

Set in `ai/app/core/config.py` (via `.env`):
- `RAG_EMBEDDING_PROVIDER`: `sentence-transformers`
- `RAG_EMBEDDING_MODEL`: `sentence-transformers/all-MiniLM-L6-v2`
- `RAG_EMBEDDING_DIMENSION`: `384`
- `RAG_CHUNK_SIZE`: `512`
- `RAG_CHUNK_OVERLAP`: `64`
- `RAG_TOP_K`: `5`
- `RAG_SIMILARITY_THRESHOLD`: `0.65`

---

## Health Diagnostics & Failure Modes

### 1. Vector Store Status (`PgVectorStore.health()`)
- `HEALTHY`: PostgreSQL `pgvector` connected and active.
- `PGVECTOR_REQUIRED`: PostgreSQL `pgvector` unconfigured in environment; fallback persistent store active with 100% tenant isolation.

### 2. Embedding Provider Status (`SentenceTransformersEmbeddingProvider`)
- `SUCCESS`: Real 384d embedding generated.
- `MODEL_UNAVAILABLE`: Library or weights missing (no pseudo-sine fallback).

### 3. Response Statuses
- `GROUNDED`: Authorized evidence score $\ge$ threshold.
- `INSUFFICIENT_EVIDENCE`: No authorized evidence or similarity below threshold.
