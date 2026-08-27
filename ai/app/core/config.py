import os
from functools import lru_cache
from typing import Optional


class AISettings:
    """Configuration settings for the AI Subsystem loaded from environment variables."""

    def __init__(self):
        self.app_name: str = os.getenv("APP_NAME", "AgentTrust-OS-AI")
        self.environment: str = os.getenv("APP_ENV", "development")
        self.debug: bool = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")

        # Provider Credentials (Loaded safely from Environment Variables)
        self.ai_api_key: Optional[str] = os.getenv("AI_API_KEY")
        self.openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")

        # Routing Defaults
        self.default_provider: str = os.getenv("AI_PROVIDER", "gemini")
        self.default_model: str = os.getenv("AI_MODEL", "gemini-1.5-flash")
        self.fallback_provider: str = os.getenv("AI_FALLBACK_PROVIDER", "mock")
        self.fallback_model: str = os.getenv("AI_FALLBACK_MODEL", "mock-deterministic-v1")

        # Execution Limits & Timeouts
        self.timeout_seconds: float = float(os.getenv("AI_TIMEOUT_SECONDS", "15.0"))
        self.max_retries: int = int(os.getenv("AI_MAX_RETRIES", "2"))
        self.retry_backoff_factor: float = 1.5

        # Safety & Guardrails Configuration
        self.pii_redaction_enabled: bool = os.getenv("PII_REDACTION_ENABLED", "true").lower() in ("true", "1", "yes")
        self.prompt_shield_enabled: bool = os.getenv("PROMPT_SHIELD_ENABLED", "true").lower() in ("true", "1", "yes")
        self.decision_guard_enabled: bool = os.getenv("DECISION_GUARD_ENABLED", "true").lower() in ("true", "1", "yes")

        # Localization
        self.default_language: str = os.getenv("DEFAULT_LANGUAGE", "en")
        self.supported_languages: str = os.getenv("SUPPORTED_LANGUAGES", "en,hi")

        # Document Perception & Vision ML Configuration
        self.ocr_provider: str = os.getenv("OCR_PROVIDER", "paddleocr")
        self.ocr_model: str = os.getenv("OCR_MODEL", "ch_PP-OCRv4_rec")
        self.ocr_use_angle_cls: bool = os.getenv("OCR_USE_ANGLE_CLS", "true").lower() in ("true", "1", "yes")
        self.yolo_model_path: str = os.getenv(
            "YOLO_MODEL_PATH",
            "runs/detect/artifacts/training/doc_layout/real_yolo_002/train_run/weights/best.pt",
        )
        self.yolo_confidence_threshold: float = float(os.getenv("YOLO_CONFIDENCE_THRESHOLD", "0.25"))
        self.yolo_iou_threshold: float = float(os.getenv("YOLO_IOU_THRESHOLD", "0.45"))
        self.yolo_device: str = os.getenv("YOLO_DEVICE", "cpu")
        self.yolo_image_size: int = int(os.getenv("YOLO_IMAGE_SIZE", "640"))
        self.document_max_size_bytes: int = int(os.getenv("DOCUMENT_MAX_SIZE", str(15 * 1024 * 1024)))
        self.document_max_pages: int = int(os.getenv("DOCUMENT_MAX_PAGES", "20"))

        # Financial ML & Anomaly Detection Configuration (Phase 2B)
        self.risk_model_path: str = os.getenv("RISK_MODEL_PATH", "")
        self.risk_model_version: str = os.getenv("RISK_MODEL_VERSION", "v1.0.0")
        self.risk_model_threshold: float = float(os.getenv("RISK_MODEL_THRESHOLD", "0.50"))
        self.risk_model_feature_schema: str = os.getenv("RISK_MODEL_FEATURE_SCHEMA", "risk_features_v1.0.0")

        self.fraud_model_path: str = os.getenv("FRAUD_MODEL_PATH", "")
        self.fraud_model_version: str = os.getenv("FRAUD_MODEL_VERSION", "v1.0.0")
        self.fraud_threshold: float = float(os.getenv("FRAUD_THRESHOLD", "0.75"))
        self.fraud_feature_schema: str = os.getenv("FRAUD_FEATURE_SCHEMA", "fraud_features_v1.0.0")

        self.anomaly_model_path: str = os.getenv("ANOMALY_MODEL_PATH", "")
        self.anomaly_model_version: str = os.getenv("ANOMALY_MODEL_VERSION", "v1.0.0")
        self.anomaly_threshold: float = float(os.getenv("ANOMALY_THRESHOLD", "0.70"))

        # Permission-Aware RAG & Knowledge Configuration (Phase 2C & 2C.1)
        self.rag_embedding_provider: str = os.getenv("RAG_EMBEDDING_PROVIDER", "sentence-transformers")
        self.rag_embedding_model: str = os.getenv("RAG_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        self.rag_embedding_dimension: int = int(os.getenv("RAG_EMBEDDING_DIMENSION", "384"))
        self.rag_chunk_size: int = int(os.getenv("RAG_CHUNK_SIZE", "512"))
        self.rag_chunk_overlap: int = int(os.getenv("RAG_CHUNK_OVERLAP", "64"))
        self.rag_top_k: int = int(os.getenv("RAG_TOP_K", "5"))
        self.rag_similarity_threshold: float = float(os.getenv("RAG_SIMILARITY_THRESHOLD", "0.65"))

        # PostgreSQL + pgvector Database Configuration
        self.pgvector_host: str = os.getenv("PGVECTOR_HOST", "")
        self.pgvector_port: int = int(os.getenv("PGVECTOR_PORT", "5432"))
        self.pgvector_database: str = os.getenv("PGVECTOR_DATABASE", "agenttrust_ai")
        self.pgvector_user: str = os.getenv("PGVECTOR_USER", "postgres")
        self.pgvector_password: str = os.getenv("PGVECTOR_PASSWORD", "")
        self.pgvector_url: str = os.getenv("PGVECTOR_URL", "")

        # Member 1 Backend Service Configuration
        self.backend_service_url: str = os.getenv("BACKEND_SERVICE_URL", "http://localhost:8000")

    def get_pgvector_dsn(self) -> str:

        """Returns PostgreSQL DSN connection string."""
        if self.pgvector_url:
            return self.pgvector_url
        if not self.pgvector_host:
            return ""
        return f"postgresql://{self.pgvector_user}:{self.pgvector_password}@{self.pgvector_host}:{self.pgvector_port}/{self.pgvector_database}"






@lru_cache()
def get_ai_settings() -> AISettings:
    return AISettings()


ai_settings = get_ai_settings()
