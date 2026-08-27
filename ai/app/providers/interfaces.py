from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field


# Category Enums / Identifiers
class ModelCategory:
    LLM = "LLM"
    REASONING_LLM = "REASONING_LLM"
    EMBEDDING_MODEL = "EMBEDDING_MODEL"
    VISION_MODEL = "VISION_MODEL"
    OCR_MODEL = "OCR_MODEL"
    RISK_MODEL = "RISK_MODEL"
    ANOMALY_MODEL = "ANOMALY_MODEL"
    CLASSIFICATION_MODEL = "CLASSIFICATION_MODEL"


# Output Models
class OCRResult(BaseModel):
    document_type: str  # e.g., "bank_statement", "pay_slip", "tax_return", "id_card"
    extracted_text: str
    key_value_pairs: Dict[str, Any] = Field(default_factory=dict)
    tables: List[List[List[str]]] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0, default=0.90)


class RiskOutput(BaseModel):
    score: int = Field(ge=0, le=1000)  # 0 to 1000 credit risk score
    risk_level: str  # "low" | "medium" | "high" | "critical"
    probability_of_default: float = Field(ge=0.0, le=1.0)
    factors: List[Dict[str, Any]] = Field(default_factory=list)
    recommendation: str  # "approve" | "review" | "reject" | "escalate"


class AnomalyOutput(BaseModel):
    is_anomaly: bool
    anomaly_score: float = Field(ge=0.0, le=1.0)  # 0 = normal, 1 = highly anomalous
    severity: str  # "info" | "warning" | "high" | "critical"
    anomalous_features: List[str] = Field(default_factory=list)


class ClassificationOutput(BaseModel):
    label: str
    confidence: float = Field(ge=0.0, le=1.0)
    probabilities: Dict[str, float] = Field(default_factory=dict)


# Abstract Provider Interfaces
class BaseLLMProvider(ABC):
    """Interface for general Large Language Models (LLM)."""
    @abstractmethod
    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None, language: str = "en") -> Tuple[str, Dict[str, Any]]:
        pass


class BaseReasoningLLMProvider(ABC):
    """Interface for complex reasoning LLMs (REASONING_LLM)."""
    @abstractmethod
    async def generate_reasoning(self, prompt: str, context: Dict[str, Any]) -> Tuple[str, List[str], Dict[str, Any]]:
        """Returns: Tuple[reasoning_text, evidence_list, metadata]"""
        pass


class BaseEmbeddingProvider(ABC):
    """Interface for Text & Vector Embedding models (EMBEDDING_MODEL)."""
    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        pass

    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        pass


class BaseVisionProvider(ABC):
    """Interface for Computer Vision & Visual Document Understanding (VISION_MODEL)."""
    @abstractmethod
    async def analyze_image(self, image_bytes: bytes, task: str) -> Dict[str, Any]:
        pass


class BaseOCRProvider(ABC):
    """Interface for Optical Character Recognition (OCR_MODEL)."""
    @abstractmethod
    async def extract_document(self, file_bytes: bytes, file_name: str) -> OCRResult:
        pass


class BaseRiskModelProvider(ABC):
    """Interface for Credit Risk & Underwriting ML models (RISK_MODEL)."""
    @abstractmethod
    async def predict_risk(self, applicant_data: Dict[str, Any]) -> RiskOutput:
        pass


class BaseAnomalyModelProvider(ABC):
    """Interface for Anomaly & Fraud Detection models (ANOMALY_MODEL)."""
    @abstractmethod
    async def detect_anomaly(self, transaction_data: Dict[str, Any], baseline_features: Dict[str, Any]) -> AnomalyOutput:
        pass


class BaseClassificationProvider(ABC):
    """Interface for General Classification models (CLASSIFICATION_MODEL)."""
    @abstractmethod
    async def classify(self, input_features: Dict[str, Any]) -> ClassificationOutput:
        pass
