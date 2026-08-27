from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel, Field


# Standard ML Output Signal Contracts
class FeatureAttribution(BaseModel):
    feature_name: str
    value: float
    importance_weight: float  # SHAP value / feature weight
    impact_direction: str  # "positive" | "negative" | "neutral"
    description: str


class RiskPredictionSignal(BaseModel):
    risk_score: int = Field(ge=300, le=850)  # 300 to 850 credit risk score
    probability_of_default: float = Field(ge=0.0, le=1.0)
    risk_level: str  # "low" | "medium" | "high" | "critical"
    confidence: float = Field(ge=0.0, le=1.0)
    attributions: List[FeatureAttribution] = Field(default_factory=list)
    suggested_decision: str  # "approve" | "review" | "reject" | "escalate"
    model_version: str


class FraudClassificationSignal(BaseModel):
    fraud_score: float = Field(ge=0.0, le=1.0)  # 0.0 = legitimate, 1.0 = highly fraudulent
    fraud_type: str  # "identity_theft" | "synthetic_account" | "velocity_spike" | "account_takeover" | "normal"
    severity: str  # "info" | "warning" | "high" | "critical"
    confidence: float = Field(ge=0.0, le=1.0)
    attributions: List[FeatureAttribution] = Field(default_factory=list)
    model_version: str


class BehaviourAnomalySignal(BaseModel):
    anomaly_score: float = Field(ge=0.0, le=1.0)
    is_anomalous: bool
    behaviour_vector: str  # "session_time_drift" | "device_switch" | "unusual_navigation" | "normal"
    severity: str  # "info" | "warning" | "high"
    confidence: float = Field(ge=0.0, le=1.0)
    anomalous_features: List[str] = Field(default_factory=list)
    model_version: str


class TransactionAnomalySignal(BaseModel):
    anomaly_score: float = Field(ge=0.0, le=1.0)
    is_anomalous: bool
    velocity_spike_ratio: float
    amount_deviation_sigma: float
    severity: str  # "info" | "warning" | "high" | "critical"
    confidence: float = Field(ge=0.0, le=1.0)
    anomalous_features: List[str] = Field(default_factory=list)
    model_version: str


class RepaymentPredictionSignal(BaseModel):
    repayment_probability: float = Field(ge=0.0, le=1.0)
    expected_delay_days: int = Field(ge=0)
    delinquency_tier: str  # "on_time" | "30_days_late" | "60_days_late" | "default_risk"
    confidence: float = Field(ge=0.0, le=1.0)
    attributions: List[FeatureAttribution] = Field(default_factory=list)
    model_version: str


# Abstract ML Interfaces
class BaseRiskPredictionModel(ABC):
    @abstractmethod
    async def predict_risk(self, applicant_features: Dict[str, Any]) -> RiskPredictionSignal:
        pass


class BaseFraudClassificationModel(ABC):
    @abstractmethod
    async def classify_fraud(self, event_features: Dict[str, Any]) -> FraudClassificationSignal:
        pass


class BaseBehaviourAnomalyModel(ABC):
    @abstractmethod
    async def detect_behaviour_anomaly(self, session_features: Dict[str, Any], user_baseline: Dict[str, Any]) -> BehaviourAnomalySignal:
        pass


class BaseTransactionAnomalyModel(ABC):
    @abstractmethod
    async def detect_transaction_anomaly(self, transaction: Dict[str, Any], historical_baseline: Dict[str, Any]) -> TransactionAnomalySignal:
        pass


class BaseRepaymentPredictionModel(ABC):
    @abstractmethod
    async def predict_repayment(self, loan_features: Dict[str, Any], payment_history: Dict[str, Any]) -> RepaymentPredictionSignal:
        pass
