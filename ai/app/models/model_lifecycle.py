import hashlib
import os
import threading
import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ModelMetadata(BaseModel):
    """Metadata representing a registered model instance."""

    model_name: str
    model_type: str  # "ocr" | "layout_detection" | "risk_classification" | "fraud_classification" | "embedding"
    version: str
    provider: str
    artifact_path: Optional[str] = None
    status: str = "CONFIGURED"  # "IMPLEMENTED" | "CONFIGURED" | "MODEL-READY" | "MOCK" | "NOT_AVAILABLE"
    is_loaded: bool = False
    device: str = "cpu"
    loaded_at: Optional[str] = None
    checksum: Optional[str] = None


class ModelRegistryManager:
    """
    Lightweight Model Lifecycle & Model Registry Manager.
    Ensures safe model loading, thread-safe instance caching, version tracking, and reproducible audit metadata.
    """

    def __init__(self):
        self._registry: Dict[str, ModelMetadata] = {}
        self._model_instances: Dict[str, Any] = {}
        self._lock = threading.Lock()
        self._initialize_default_registry()

    def _initialize_default_registry(self):
        """Initializes default model entries in the registry."""
        self.register_model(
            ModelMetadata(
                model_name="PaddleOCR-v4",
                model_type="ocr",
                version="v4.0",
                provider="paddleocr",
                artifact_path=os.getenv("OCR_MODEL", "ch_PP-OCRv4_rec"),
                status="CONFIGURED",
                is_loaded=False,
            )
        )
        self.register_model(
            ModelMetadata(
                model_name="YOLOv8-DocLayout",
                model_type="layout_detection",
                version="v8.0",
                provider="ultralytics",
                artifact_path=os.getenv("YOLO_MODEL_PATH", ""),
                status="NOT_AVAILABLE" if not os.getenv("YOLO_MODEL_PATH") else "CONFIGURED",
                is_loaded=False,
            )
        )
        self.register_model(
            ModelMetadata(
                model_name="XGBoost-CreditRisk",
                model_type="risk_classification",
                version="v1.0",
                provider="xgboost",
                artifact_path=os.getenv("RISK_MODEL_PATH", ""),
                status="NOT_AVAILABLE" if not os.getenv("RISK_MODEL_PATH") else "CONFIGURED",
                is_loaded=False,
            )
        )
        self.register_model(
            ModelMetadata(
                model_name="LightGBM-FraudClassifier",
                model_type="fraud_classification",
                version="v1.0",
                provider="lightgbm",
                artifact_path=os.getenv("FRAUD_MODEL_PATH", ""),
                status="NOT_AVAILABLE" if not os.getenv("FRAUD_MODEL_PATH") else "CONFIGURED",
                is_loaded=False,
            )
        )
        self.register_model(
            ModelMetadata(
                model_name="IsolationForest-AnomalyDetector",
                model_type="anomaly_detection",
                version="v1.0",
                provider="scikit-learn",
                artifact_path=os.getenv("ANOMALY_MODEL_PATH", ""),
                status="NOT_AVAILABLE" if not os.getenv("ANOMALY_MODEL_PATH") else "CONFIGURED",
                is_loaded=False,
            )
        )
        self.register_model(
            ModelMetadata(
                model_name="SentenceTransformers-Embedding",
                model_type="embedding",
                version="all-MiniLM-L6-v2",
                provider="sentence-transformers",
                artifact_path=os.getenv("RAG_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"),
                status="CONFIGURED",
                is_loaded=False,
            )
        )



    def register_model(self, metadata: ModelMetadata):
        """Registers or updates model metadata in the registry."""
        with self._lock:
            self._registry[metadata.model_name] = metadata

    def get_metadata(self, model_name: str) -> Optional[ModelMetadata]:
        """Retrieves model metadata by name."""
        with self._lock:
            return self._registry.get(model_name)

    def set_loaded_instance(self, model_name: str, instance: Any, artifact_path: Optional[str] = None):
        """Caches a loaded model instance in memory."""
        with self._lock:
            self._model_instances[model_name] = instance
            if model_name in self._registry:
                meta = self._registry[model_name]
                meta.is_loaded = True
                meta.status = "MODEL-READY"
                meta.loaded_at = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
                if artifact_path:
                    meta.artifact_path = artifact_path
                    if os.path.exists(artifact_path) and os.path.isfile(artifact_path):
                        meta.checksum = self._calculate_checksum(artifact_path)

    def get_loaded_instance(self, model_name: str) -> Optional[Any]:
        """Retrieves cached loaded model instance if available."""
        with self._lock:
            return self._model_instances.get(model_name)

    def list_all_models(self) -> List[ModelMetadata]:
        """Returns all registered model metadata."""
        with self._lock:
            return list(self._registry.values())

    def _calculate_checksum(self, filepath: str) -> str:
        """Calculates MD5 checksum for a model artifact file."""
        try:
            hasher = hashlib.md5()
            with open(filepath, "rb") as f:
                buf = f.read(65536)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = f.read(65536)
            return hasher.hexdigest()
        except Exception:
            return "unknown"


model_registry_manager = ModelRegistryManager()
