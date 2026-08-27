# AI RAG Data Model & Schema Specification - AgentTrust OS

**Author**: Member 3 (AI/ML/LLM/Agent Intelligence Subsystem Lead)  
**Date**: August 25, 2026  
**Scope**: Schema definitions for chunks, metadata, requests, and responses

---

## Data Model Schemas

### 1. Document Chunk Authorization Metadata ([`ChunkAuthorizationMetadata`](file:///d:/Agenttrust-os-/ai/app/rag/schema.py))
- `document_id`: Unique identifier for document file.
- `document_type`: `"bank_policy"`, `"product_rule"`, `"governance_policy"`, `"financial_document"`.
- `organization_id`: Multi-tenant organization scope.
- `user_id`: Optional private user scope.
- `allowed_roles`: List of roles (`["user", "banker"]`).
- `data_sensitivity`: `"public"`, `"internal"`, `"confidential"`, `"restricted"`.
- `consent_given`: Boolean flag indicating customer consent.
- `is_deleted`: Boolean soft-deletion flag.
- `policy_version`: Version string (e.g. `"1.0.0"`).
- `is_active_version`: Active version indicator.

### 2. Document Chunk ([`DocumentChunk`](file:///d:/Agenttrust-os-/ai/app/rag/schema.py))
- `chunk_id`: Unique chunk identifier (`chk_{doc_id}_{idx}`).
- `text`: Extracted chunk text.
- `embedding`: 384-dimensional dense float vector.
- `metadata`: [`ChunkAuthorizationMetadata`](file:///d:/Agenttrust-os-/ai/app/rag/schema.py).

### 3. RAG Response ([`RAGResponse`](file:///d:/Agenttrust-os-/ai/app/rag/schema.py))
- `answer`: Grounded response text.
- `citations`: List of [`Citation`](file:///d:/Agenttrust-os-/ai/app/rag/schema.py) objects (`document_id`, `snippet`, `relevance_score`).
- `grounded`: Boolean flag.
- `grounding_status`: `"GROUNDED"`, `"PARTIALLY_GROUNDED"`, `"INSUFFICIENT_EVIDENCE"`.
- `requires_human_review`: Boolean flag.
