from typing import List, Tuple
from ai.app.core.config import ai_settings
from ai.app.rag.schema import Citation, DocumentChunk, RAGQueryRequest, RAGResponse


class RAGGenerator:
    """Generates grounded responses with explicit evidence citations and hallucination controls."""

    def generate_response(
        self,
        request: RAGQueryRequest,
        sanitized_chunks: List[Tuple[DocumentChunk, float]],
        filtered_count: int,
        injection_detected: bool,
    ) -> RAGResponse:
        citations: List[Citation] = []
        context_snippets = []

        for chunk, score in sanitized_chunks:
            meta = chunk.metadata
            snippet = chunk.text[:150] + ("..." if len(chunk.text) > 150 else "")
            context_snippets.append(snippet)

            citations.append(
                Citation(
                    document_id=meta.document_id,
                    document_type=meta.document_type,
                    policy_version=meta.policy_version,
                    snippet=snippet,
                    relevance_score=score,
                )
            )

        if not sanitized_chunks:
            answer = (
                f"INSUFFICIENT_EVIDENCE: No authorized document content was found matching query '{request.query_text}' "
                f"for tenant '{request.organization_id}' under role '{request.role}'."
            )
            grounding_status = "INSUFFICIENT_EVIDENCE"
            grounded = False
        else:
            top_score = citations[0].relevance_score
            if top_score < 0.20:
                answer = (
                    f"INSUFFICIENT_EVIDENCE: Retrieved document relevance score ({top_score}) is below threshold "
                    f"({ai_settings.rag_similarity_threshold}). No grounded evidence available."
                )
                grounding_status = "INSUFFICIENT_EVIDENCE"
                grounded = False
            else:
                answer = (
                    f"Based on authorized {citations[0].document_type} (version {citations[0].policy_version}): "
                    f"{context_snippets[0]}"
                )
                grounding_status = "GROUNDED"
                grounded = True

        return RAGResponse(
            answer=answer,
            citations=citations,
            chunks_retrieved_count=len(sanitized_chunks),
            chunks_filtered_count=filtered_count,
            prompt_injection_detected=injection_detected,
            grounded=grounded,
            grounding_status=grounding_status,
            requires_human_review=not grounded or injection_detected,
            model_metadata={
                "retrieval_strategy": "permission_aware_metadata_vector_search",
                "organization_id": request.organization_id,
                "role": request.role,
                "embedding_model": ai_settings.rag_embedding_model,
            },
        )


rag_generator = RAGGenerator()
