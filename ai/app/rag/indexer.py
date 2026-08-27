from typing import Any, Dict, List, Optional, Tuple
from ai.app.rag.schema import DocumentChunk
from ai.app.rag.vector_store import BaseVectorStore, file_vector_store, pg_vector_store


class VectorStoreIndexer:
    """
    Vector Store Indexer Adapter.
    Uses authoritative production PgVectorStore by default.
    Allows explicit set_store() for offline unit testing.
    """

    def __init__(self, store: Optional[BaseVectorStore] = None):
        self._store = store or pg_vector_store

    def set_store(self, store: BaseVectorStore):
        """Sets active vector store backend (e.g. file_vector_store for unit tests)."""
        self._store = store

    def get_store(self) -> BaseVectorStore:
        return self._store

    def index_chunks(self, chunks: List[DocumentChunk]):
        """Indexes document chunks into active vector storage."""
        self._store.upsert(chunks)

    def search_raw(
        self, query_text: str, organization_id: str, query_embedding: Optional[List[float]] = None, top_k: int = 20
    ) -> List[Tuple[DocumentChunk, float]]:
        """
        Delegates vector similarity search with HARD TENANT ISOLATION.
        """
        return self._store.search(
            query_embedding=query_embedding or [],
            query_text=query_text,
            organization_id=organization_id,
            top_k=top_k,
        )

    def delete_document(self, document_id: str, organization_id: str) -> int:
        """Deletes/deactivates all chunks associated with document_id."""
        return self._store.delete_document(document_id, organization_id)

    def deactivate_document_version(self, document_id: str, organization_id: str) -> int:
        """Deactivates active version state for document_id."""
        return self._store.deactivate_document_version(document_id, organization_id)

    def clear(self):
        if hasattr(self._store, "clear"):
            self._store.clear()


vector_store_indexer = VectorStoreIndexer()
