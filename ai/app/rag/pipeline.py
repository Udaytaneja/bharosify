import time
import uuid
from typing import List
from ai.app.core.config import ai_settings
from ai.app.rag.audit_logger import rag_audit_logger
from ai.app.rag.chunker import metadata_chunker
from ai.app.rag.context_filter import context_filter
from ai.app.rag.generator import rag_generator
from ai.app.rag.indexer import vector_store_indexer
from ai.app.rag.parser import document_parser
from ai.app.rag.retriever import permission_aware_retriever
from ai.app.rag.schema import ChunkAuthorizationMetadata, DocumentChunk, RAGQueryRequest, RAGResponse


class SecureRAGPipeline:
    """
    10-Stage Permission-Aware RAG Pipeline:
    Document -> Parse -> Chunk -> Metadata -> Real Embedding -> Persistent Vector Storage ->
    Permission-Aware Retrieval -> Context Filtering -> LLM -> Citation/Evidence -> Structured Response
    """

    def ingest_document(self, text_content: str, auth_metadata: ChunkAuthorizationMetadata) -> List[DocumentChunk]:
        """
        Parses, chunks, embeds, and indexes a document with mandatory authorization metadata.
        """
        clean_text, doc_meta = document_parser.parse(
            text_content=text_content,
            document_type=auth_metadata.document_type,
            document_id=auth_metadata.document_id,
        )

        chunks = metadata_chunker.chunk_document(clean_text, auth_metadata)
        vector_store_indexer.index_chunks(chunks)
        return chunks

    def delete_document(self, document_id: str, organization_id: str) -> int:
        """Deletes/deactivates document chunks across vector index."""
        return vector_store_indexer.delete_document(document_id, organization_id)

    def query(self, request: RAGQueryRequest) -> RAGResponse:
        """
        Executes permission-aware RAG query.
        """
        start_time = time.time()
        req_id = f"rag_req_{uuid.uuid4().hex[:10]}"

        # Stage 6: Pre-LLM Permission-Aware Retrieval
        retrieved_chunks, filtered_count = permission_aware_retriever.retrieve(request)

        # Stage 7: Context Filtering & Indirect Prompt Injection Sanitization
        sanitized_chunks, injection_detected = context_filter.filter_and_sanitize(retrieved_chunks)

        # Stage 8, 9, 10: LLM Generation, Citations, & Structured Response
        response = rag_generator.generate_response(
            request=request,
            sanitized_chunks=sanitized_chunks,
            filtered_count=filtered_count,
            injection_detected=injection_detected,
        )

        latency_ms = (time.time() - start_time) * 1000.0

        # RAG Audit Logging
        doc_ids = list({c[0].metadata.document_id for c in sanitized_chunks})
        chunk_ids = [c[0].chunk_id for c in sanitized_chunks]

        rag_audit_logger.log_event(
            request_id=req_id,
            organization_id=request.organization_id,
            user_id=request.user_id,
            query_text=request.query_text,
            retrieved_document_ids=doc_ids,
            retrieved_chunk_ids=chunk_ids,
            embedding_model=ai_settings.rag_embedding_model,
            latency_ms=latency_ms,
            result_status=response.grounding_status,
        )

        return response


secure_rag_pipeline = SecureRAGPipeline()
