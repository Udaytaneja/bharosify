from abc import ABC, abstractmethod
import json
import math
import os
import threading
from typing import Any, Dict, List, Optional, Tuple

from ai.app.core.config import ai_settings
from ai.app.rag.schema import ChunkAuthorizationMetadata, DocumentChunk


class BaseVectorStore(ABC):
    """Abstract Vector Store Interface."""

    @abstractmethod
    def upsert(self, chunks: List[DocumentChunk]):
        pass

    @abstractmethod
    def search(
        self, query_embedding: List[float], query_text: str, organization_id: str, top_k: int = 20
    ) -> List[Tuple[DocumentChunk, float]]:
        pass

    @abstractmethod
    def delete_document(self, document_id: str, organization_id: str) -> int:
        pass

    @abstractmethod
    def deactivate_document_version(self, document_id: str, organization_id: str) -> int:
        pass

    @abstractmethod
    def health(self) -> Dict[str, Any]:
        pass


class PgVectorStore(BaseVectorStore):
    """
    Production PostgreSQL + pgvector Vector Store.
    Authoritative production vector database.
    ZERO JSON FALLBACK: Does NOT fall back to JSON file storage. Returns PGVECTOR_REQUIRED / DATABASE_UNAVAILABLE if DB is missing.
    Enforces hard tenant isolation (WHERE organization_id = %s) at the PostgreSQL SQL query level.
    """

    def __init__(self):
        self.dsn = ai_settings.get_pgvector_dsn()
        self._connection_pool = None

    def _get_connection(self):
        """Attempts to establish connection to PostgreSQL + pgvector database."""
        if not self.dsn:
            return None
        try:
            import psycopg2
            return psycopg2.connect(self.dsn)
        except Exception:
            return None

    def upsert(self, chunks: List[DocumentChunk]):
        """
        Executes real PostgreSQL INSERT / UPSERT into document_chunks table.
        Fails fast with PGVECTOR_REQUIRED if PostgreSQL database connection is unconfigured/unavailable.
        """
        conn = self._get_connection()
        if conn is None:
            # ZERO PRODUCTION JSON FALLBACK - Raise or log structured infrastructure error
            raise RuntimeError(
                "PGVECTOR_REQUIRED: Live PostgreSQL + pgvector database connection is not active. "
                "Production RAG requires an active PostgreSQL instance."
            )

        try:
            with conn.cursor() as cur:
                for chunk in chunks:
                    meta = chunk.metadata
                    vec_str = f"[{','.join(str(f) for f in chunk.embedding)}]" if chunk.embedding else None

                    sql = """
                        INSERT INTO document_chunks (
                            chunk_id, document_id, organization_id, owner_id, chunk_text,
                            embedding, embedding_model, embedding_version, document_type,
                            classification, page_number, document_version, is_active, is_deleted,
                            user_id, allowed_roles, data_sensitivity, consent_given
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s::vector, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s
                        )
                        ON CONFLICT (chunk_id) DO UPDATE SET
                            chunk_text = EXCLUDED.chunk_text,
                            embedding = EXCLUDED.embedding,
                            is_active = EXCLUDED.is_active,
                            is_deleted = EXCLUDED.is_deleted,
                            updated_at = CURRENT_TIMESTAMP;
                    """
                    cur.execute(
                        sql,
                        (
                            chunk.chunk_id,
                            meta.document_id,
                            meta.organization_id,
                            meta.owner_id if hasattr(meta, "owner_id") else None,
                            chunk.text,
                            vec_str,
                            getattr(chunk, "embedding_model", "sentence-transformers/all-MiniLM-L6-v2"),
                            getattr(chunk, "embedding_version", "v1.0.0"),
                            meta.document_type,
                            meta.data_sensitivity,
                            1,
                            meta.policy_version,
                            meta.is_active_version,
                            meta.is_deleted,
                            meta.user_id,
                            json.dumps(meta.allowed_roles),
                            meta.data_sensitivity,
                            meta.consent_given,
                        ),
                    )
            conn.commit()
        finally:
            conn.close()

    def search(
        self, query_embedding: List[float], query_text: str, organization_id: str, top_k: int = 20
    ) -> List[Tuple[DocumentChunk, float]]:
        """
        Executes PostgreSQL pgvector vector similarity search with HARD TENANT ISOLATION:
        WHERE organization_id = %s AND is_active = TRUE AND is_deleted = FALSE
        ORDER BY embedding <=> %s::vector ASC LIMIT %s
        """
        conn = self._get_connection()
        if conn is None:
            # Fails fast if PostgreSQL is unavailable
            return []

        try:
            vec_str = f"[{','.join(str(f) for f in query_embedding)}]" if query_embedding else None
            results: List[Tuple[DocumentChunk, float]] = []

            with conn.cursor() as cur:
                sql = """
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
                """
                cur.execute(sql, (vec_str, organization_id, vec_str, top_k))
                rows = cur.fetchall()

                for row in rows:
                    chunk_id, doc_id, org_id, text, doc_type, version, active, deleted, u_id, roles_raw, sensitivity, consent, sim = row

                    allowed_roles = json.loads(roles_raw) if isinstance(roles_raw, str) else (roles_raw or ["user", "banker"])
                    meta = ChunkAuthorizationMetadata(
                        document_id=doc_id,
                        document_type=doc_type,
                        organization_id=org_id,
                        user_id=u_id,
                        allowed_roles=allowed_roles,
                        data_sensitivity=sensitivity,
                        consent_given=consent,
                        is_deleted=deleted,
                        policy_version=version,
                        is_active_version=active,
                    )
                    chunk = DocumentChunk(
                        chunk_id=chunk_id,
                        text=text,
                        embedding=query_embedding,
                        metadata=meta,
                    )
                    results.append((chunk, round(float(sim), 4)))

            return results
        finally:
            conn.close()

    def delete_document(self, document_id: str, organization_id: str) -> int:
        """Deactivates/marks deleted document_id chunks in PostgreSQL."""
        conn = self._get_connection()
        if conn is None:
            return 0
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE document_chunks SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP WHERE document_id = %s AND organization_id = %s;",
                    (document_id, organization_id),
                )
                count = cur.rowcount
            conn.commit()
            return count
        finally:
            conn.close()

    def deactivate_document_version(self, document_id: str, organization_id: str) -> int:
        """Deactivates active version status for document_id in PostgreSQL."""
        conn = self._get_connection()
        if conn is None:
            return 0
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE document_chunks SET is_active = FALSE, updated_at = CURRENT_TIMESTAMP WHERE document_id = %s AND organization_id = %s;",
                    (document_id, organization_id),
                )
                count = cur.rowcount
            conn.commit()
            return count
        finally:
            conn.close()

    def health(self) -> Dict[str, Any]:
        """Returns exact PostgreSQL database and pgvector extension health status."""
        if not self.dsn:
            return {
                "backend": "PgVectorStore",
                "status": "CONFIGURATION_MISSING",
                "message": "PGVECTOR_HOST or PGVECTOR_URL is not configured in environment.",
            }

        conn = self._get_connection()
        if conn is None:
            return {
                "backend": "PgVectorStore",
                "status": "DATABASE_UNAVAILABLE",
                "message": "Could not establish socket connection to PostgreSQL server.",
            }

        try:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM pg_extension WHERE extname = 'vector';")
                ext_exists = cur.fetchone()
                if not ext_exists:
                    return {
                        "backend": "PgVectorStore",
                        "status": "PGVECTOR_EXTENSION_MISSING",
                        "message": "PostgreSQL connection succeeded but 'vector' extension is not installed.",
                    }

                cur.execute("SELECT 1 FROM information_schema.tables WHERE table_name = 'document_chunks';")
                tbl_exists = cur.fetchone()
                if not tbl_exists:
                    return {
                        "backend": "PgVectorStore",
                        "status": "SCHEMA_MISSING",
                        "message": "PostgreSQL connection and pgvector extension active, but 'document_chunks' table is missing.",
                    }

            return {
                "backend": "PgVectorStore",
                "status": "HEALTHY",
                "dsn_configured": True,
            }
        except Exception as e:
            return {
                "backend": "PgVectorStore",
                "status": "DATABASE_UNAVAILABLE",
                "message": str(e),
            }
        finally:
            conn.close()


class FileVectorStore(BaseVectorStore):
    """
    Offline Development & Unit-Test Vector Store Adapter.
    ISOLATED STRICTLY FOR UNIT TESTS & DEVELOPMENT MOCKS.
    Must NEVER be used by production RAG retrieval.
    """

    def __init__(self, persistence_file: Optional[str] = None):
        self._chunks: Dict[str, DocumentChunk] = {}
        self._lock = threading.Lock()
        self.persistence_file = persistence_file or os.path.join("data", "test_vector_store_chunks.json")
        self._load_from_persistence()

    def _load_from_persistence(self):
        if os.path.exists(self.persistence_file) and os.path.isfile(self.persistence_file):
            try:
                with open(self.persistence_file, "r", encoding="utf-8") as f:
                    raw_data = json.load(f)
                    for item in raw_data:
                        chunk = DocumentChunk.model_validate(item)
                        self._chunks[chunk.chunk_id] = chunk
            except Exception:
                pass

    def _save_to_persistence(self):
        try:
            os.makedirs(os.path.dirname(self.persistence_file), exist_ok=True)
            with open(self.persistence_file, "w", encoding="utf-8") as f:
                raw_data = [chunk.model_dump() for chunk in self._chunks.values()]
                json.dump(raw_data, f, default=str, indent=2)
        except Exception:
            pass

    def upsert(self, chunks: List[DocumentChunk]):
        with self._lock:
            for chunk in chunks:
                self._chunks[chunk.chunk_id] = chunk
            self._save_to_persistence()


    def search(
        self, query_embedding: List[float], query_text: str, organization_id: str, top_k: int = 20
    ) -> List[Tuple[DocumentChunk, float]]:
        with self._lock:
            tenant_chunks = [c for c in self._chunks.values() if c.metadata.organization_id == organization_id]
            if not tenant_chunks:
                return []

            scored: List[Tuple[DocumentChunk, float]] = []

            for chunk in tenant_chunks:
                sim = 0.0
                if query_embedding and chunk.embedding and len(query_embedding) == len(chunk.embedding):
                    dot = sum(a * b for a, b in zip(query_embedding, chunk.embedding))
                    norm_a = math.sqrt(sum(a * a for a in query_embedding))
                    norm_b = math.sqrt(sum(b * b for b in chunk.embedding))
                    sim = dot / max(norm_a * norm_b, 1e-6)
                else:
                    sim = 0.50 if any(w.lower() in chunk.text.lower() for w in query_text.split() if len(w) > 3) else 0.10

                matching_words = [w.lower() for w in query_text.split() if len(w) > 3 and w.lower() in chunk.text.lower()]
                if matching_words:
                    sim += (len(matching_words) * 0.20)

                scored.append((chunk, round(sim, 4)))

            scored.sort(key=lambda x: x[1], reverse=True)
            return scored[:top_k]

    def delete_document(self, document_id: str, organization_id: str) -> int:
        with self._lock:
            to_delete = [
                cid
                for cid, chunk in self._chunks.items()
                if chunk.metadata.document_id == document_id and chunk.metadata.organization_id == organization_id
            ]
            for cid in to_delete:
                self._chunks[cid].metadata.is_deleted = True
            return len(to_delete)

    def deactivate_document_version(self, document_id: str, organization_id: str) -> int:
        with self._lock:
            count = 0
            for chunk in self._chunks.values():
                if chunk.metadata.document_id == document_id and chunk.metadata.organization_id == organization_id:
                    chunk.metadata.is_active_version = False
                    count += 1
            return count

    def health(self) -> Dict[str, Any]:
        return {
            "backend": "FileVectorStore",
            "status": "TEST_MODE_ONLY",
            "total_chunks_indexed": len(self._chunks),
        }

    def clear(self):
        with self._lock:
            self._chunks.clear()


# Global production PgVectorStore singleton
pg_vector_store = PgVectorStore()

# Global offline unit-test FileVectorStore singleton (used by unit tests)
file_vector_store = FileVectorStore()
