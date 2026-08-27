from decimal import Decimal
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class UnderwritingAssessmentRequest(BaseModel):
    banker_id: str
    organization_id: str
    applicant_id: str
    language: Optional[str] = "en"  # "en" | "hi" | "hinglish"
    question: str


class UnderwritingFactItem(BaseModel):
    category: str  # "INCOME" | "EXPENSES" | "DEBT" | "SAVINGS" | "ASSETS"
    label: str
    value: str  # Exact format e.g. "₹1,00,000.00"
    source: str = "Member 1 Authoritative Financial API"


class UnderwritingRiskFactorItem(BaseModel):
    factor_id: str
    severity: str  # "HIGH" | "MEDIUM" | "LOW"
    description: str
    evidence_type: str  # "FACT" | "CALCULATION" | "MODEL_SIGNAL" | "POLICY"


class UnderwritingPositiveFactorItem(BaseModel):
    factor_id: str
    description: str
    impact: str = "STABILIZING"


class UnderwritingFraudSignalItem(BaseModel):
    signal_type: str
    severity: str  # "HIGH" | "MEDIUM" | "LOW"
    score: float
    description: str
    status: str = "EXPERIMENTAL"


class UnderwritingAnomalySignalItem(BaseModel):
    anomaly_type: str
    score: float
    detected_behavior: str
    status: str = "EXPERIMENTAL"


class UnderwritingPolicyEvidenceItem(BaseModel):
    document_id: str
    policy_name: str
    clause: str
    compliance_status: str  # "COMPLIANT" | "NON_COMPLIANT" | "REQUIRES_SENIOR_APPROVAL"
    relevance_score: float


class UnderwritingDocumentEvidenceItem(BaseModel):
    document_type: str  # "SALARY_SLIP" | "BANK_STATEMENT" | "IDENTITY"
    verification_status: str  # "VERIFIED" | "SUSPICIOUS" | "UNVERIFIED"
    detected_fields: Dict[str, Any] = Field(default_factory=dict)
    confidence: float
    layout_regions: List[Dict[str, Any]] = Field(default_factory=list)
    ocr_lines: List[Dict[str, Any]] = Field(default_factory=list)
    provenance: Dict[str, Any] = Field(default_factory=dict)


class UnderwritingModelSignalItem(BaseModel):
    model_name: str
    model_version: str
    status: str = "EXPERIMENTAL"
    score: float
    confidence: float
    reason_codes: List[str] = Field(default_factory=list)
    disclaimer: str = "EXPERIMENTAL BENCHMARK MODEL. Non-authoritative."


class UnderwritingAssessment(BaseModel):
    assessment_id: str
    applicant_id: str
    organization_id: str
    overall_risk: str  # "LOW" | "MODERATE" | "HIGH" | "CRITICAL"
    risk_score: float  # 0.0 - 1.0
    trust_score: int  # 0 - 100
    financial_facts: List[UnderwritingFactItem] = Field(default_factory=list)
    risk_factors: List[UnderwritingRiskFactorItem] = Field(default_factory=list)
    positive_factors: List[UnderwritingPositiveFactorItem] = Field(default_factory=list)
    fraud_signals: List[UnderwritingFraudSignalItem] = Field(default_factory=list)
    anomaly_signals: List[UnderwritingAnomalySignalItem] = Field(default_factory=list)
    policy_evidence: List[UnderwritingPolicyEvidenceItem] = Field(default_factory=list)
    document_evidence: List[UnderwritingDocumentEvidenceItem] = Field(default_factory=list)
    model_signals: List[UnderwritingModelSignalItem] = Field(default_factory=list)
    ai_explanation: str
    recommended_review_items: List[str] = Field(default_factory=list)
    requires_human_review: bool = True
