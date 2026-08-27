from abc import ABC, abstractmethod
import math
import os
import time
from typing import Any, Dict, List, Optional, Tuple

from ai.app.core.config import ai_settings
from ai.app.models.model_lifecycle import model_registry_manager


from pydantic import BaseModel


class EmbeddingResult(BaseModel):
    text: str
    vector: List[float] = []



class BaseEmbeddingProvider(ABC):
    """Abstract Base Class for Vector Embedding Providers."""

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        pass

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        pass


class SentenceTransformersEmbeddingProvider(BaseEmbeddingProvider):
    """
    Production SentenceTransformers Embedding Provider Adapter.
    Generates real dense 384-dimensional text embeddings using sentence-transformers/all-MiniLM-L6-v2.
    If dependencies or model weights are missing, returns status MODEL_UNAVAILABLE
    without generating pseudo-sine or fake deterministic vectors.
    """

    def __init__(self):
        self.model_name = "SentenceTransformers-Embedding"
        self.model_identifier = ai_settings.rag_embedding_model
        self.dimension = ai_settings.rag_embedding_dimension

    def _get_or_load_st(self) -> Tuple[Optional[Any], bool, str]:
        """Retrieves cached SentenceTransformer instance or initializes once safely."""
        cached = model_registry_manager.get_loaded_instance(self.model_name)
        if cached is not None:
            return cached, True, "MODEL-READY"

        try:
            from sentence_transformers import SentenceTransformer

            st_instance = SentenceTransformer(self.model_identifier)
            model_registry_manager.set_loaded_instance(self.model_name, st_instance)
            return st_instance, True, "MODEL-READY"
        except ImportError:
            return None, False, "sentence-transformers library is not installed in runtime environment."
        except Exception as e:
            return None, False, f"SentenceTransformer loading failed: {str(e)}"

    def embed_text(self, text: str, mock_override_vector: Optional[List[float]] = None) -> Tuple[List[float], Dict[str, Any]]:
        """
        Embeds a single string query into a 384d dense vector.
        Returns: Tuple[embedding_vector, metadata]
        """
        start_time = time.time()

        if mock_override_vector is not None:
            latency_ms = (time.time() - start_time) * 1000.0
            meta = {
                "provider": self.model_name,
                "model": self.model_identifier,
                "dimension": len(mock_override_vector),
                "is_available": True,
                "latency_ms": round(latency_ms, 2),
                "status": "SUCCESS",
            }
            return mock_override_vector, meta

        st_instance, is_available, status_msg = self._get_or_load_st()
        if not is_available or st_instance is None:
            latency_ms = (time.time() - start_time) * 1000.0
            meta = {
                "provider": self.model_name,
                "model": self.model_identifier,
                "dimension": self.dimension,
                "is_available": False,
                "status_message": status_msg,
                "latency_ms": round(latency_ms, 2),
                "status": "MODEL_UNAVAILABLE",
            }
            return [], meta

        try:
            vec = st_instance.encode(text, convert_to_numpy=True).tolist()
            latency_ms = (time.time() - start_time) * 1000.0
            meta = {
                "provider": self.model_name,
                "model": self.model_identifier,
                "dimension": len(vec),
                "is_available": True,
                "latency_ms": round(latency_ms, 2),
                "status": "SUCCESS",
            }
            return vec, meta
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000.0
            meta = {
                "provider": self.model_name,
                "model": self.model_identifier,
                "dimension": self.dimension,
                "is_available": True,
                "status_message": f"Embedding generation failed: {str(e)}",
                "latency_ms": round(latency_ms, 2),
                "status": "EMBEDDING_FAILURE",
            }
            return [], meta

    def embed_documents(self, texts: List[str]) -> Tuple[List[List[float]], Dict[str, Any]]:
        """Embeds a list of document strings into dense vectors."""
        results = []
        last_meta = {}
        for t in texts:
            vec, meta = self.embed_text(t)
            results.append(vec)
            last_meta = meta
        return results, last_meta


sentence_transformers_embedding_provider = SentenceTransformersEmbeddingProvider()
