import math
from typing import List
from ai.app.providers.interfaces import BaseEmbeddingProvider


class VectorEmbeddingAdapter(BaseEmbeddingProvider):
    """Adapter for Vector Embedding models (EMBEDDING_MODEL)."""

    def __init__(self, dimension: int = 384):
        self.dimension = dimension

    async def embed_text(self, text: str) -> List[float]:
        """Generates deterministic test vector embedding representation."""
        seed = sum(ord(c) for c in text)
        return [round(math.sin(seed + i), 4) for i in range(self.dimension)]

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [await self.embed_text(t) for t in texts]
