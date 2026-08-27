from typing import List
from ai.app.core.config import ai_settings
from ai.app.rag.embedding import sentence_transformers_embedding_provider
from ai.app.rag.schema import ChunkAuthorizationMetadata, DocumentChunk


class MetadataChunker:
    """Semantic Chunker binding strict Authorization Metadata and real embeddings to EVERY chunk."""

    def __init__(self, chunk_size: int = None, overlap: int = None):
        self.chunk_size = chunk_size or ai_settings.rag_chunk_size
        self.overlap = overlap or ai_settings.rag_chunk_overlap

    def chunk_document(self, text: str, auth_meta: ChunkAuthorizationMetadata) -> List[DocumentChunk]:
        """
        Splits document text into overlapping chunks bound with ChunkAuthorizationMetadata.
        """
        words = text.split()
        if not words:
            return []

        chunks: List[DocumentChunk] = []
        i = 0
        chunk_idx = 0

        while i < len(words):
            chunk_words = words[i : i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            chunk_id = f"chk_{auth_meta.document_id}_{chunk_idx}"

            # Real 384d embedding vector generation
            embedding, embed_meta = sentence_transformers_embedding_provider.embed_text(chunk_text)

            # CRITICAL: Every chunk copies the full authorization metadata
            meta_copy = auth_meta.model_copy()

            chunks.append(
                DocumentChunk(
                    chunk_id=chunk_id,
                    text=chunk_text,
                    embedding=embedding or [],
                    metadata=meta_copy,
                )
            )

            i += max(1, self.chunk_size - self.overlap)
            chunk_idx += 1

        return chunks


metadata_chunker = MetadataChunker()
