# Banker Intelligence & Underwriting Copilot API Specification - AgentTrust OS

**Author**: Member 3 (AI/ML/LLM/Agent Intelligence Lead)  
**Date**: August 25, 2026  
**Scope**: OpenAPI Endpoint Specification for Backend Integration

---

## Endpoint Specification

### `POST /ai/banker/underwriting`

#### Request Schema ([`UnderwritingAssessmentRequest`](file:///d:/Agenttrust-os-/ai/app/schemas/underwriting.py))
```json
{
  "banker_id": "banker_101",
  "organization_id": "org_A",
  "applicant_id": "101",
  "language": "en",
  "question": "Why is this applicant risky?"
}
```

#### Response Schema ([`UnderwritingAssessment`](file:///d:/Agenttrust-os-/ai/app/schemas/underwriting.py))
```json
{
  "assessment_id": "und_ast_d42543674e",
  "applicant_id": "101",
  "organization_id": "org_A",
  "overall_risk": "MODERATE",
  "risk_score": 0.6,
  "trust_score": 94,
  "financial_facts": [
    {"category": "INCOME", "label": "Monthly Income", "value": "₹1,00,000.00", "source": "Member 1 Authoritative Financial API"},
    {"category": "EXPENSES", "label": "Monthly Expenses", "value": "₹40,000.00", "source": "Member 1 Authoritative Financial API"},
    {"category": "DEBT", "label": "Existing Loans Obligation", "value": "₹10,000.00", "source": "Member 1 Authoritative Financial API"},
    {"category": "SAVINGS", "label": "Liquid Savings", "value": "₹2,00,000.00", "source": "Member 1 Authoritative Financial API"}
  ],
  "risk_factors": [
    {
      "factor_id": "RF_HIGH_DTI",
      "severity": "HIGH",
      "description": "Debt-to-Income ratio (56.73%) exceeds 50% threshold.",
      "evidence_type": "CALCULATION"
    }
  ],
  "positive_factors": [
    {
      "factor_id": "PF_SAVINGS_BUFFER",
      "description": "Liquid savings of ₹2,00,000.00 covers over 3 months of expenses.",
      "impact": "STABILIZING"
    }
  ],
  "fraud_signals": [
    {
      "signal_type": "VOLATILITY_CHECK",
      "severity": "LOW",
      "score": 0.05,
      "description": "Transaction pattern within normal volatility parameters.",
      "status": "EXPERIMENTAL"
    }
  ],
  "anomaly_signals": [],
  "policy_evidence": [
    {
      "document_id": "doc_policy_01",
      "policy_name": "Bank Credit Policy v2.1",
      "clause": "Maximum DTI limit restricted to 50% unless senior credit committee approval is granted.",
      "compliance_status": "REQUIRES_SENIOR_APPROVAL",
      "relevance_score": 0.92
    }
  ],
  "document_evidence": [
    {
      "document_type": "SALARY_SLIP",
      "verification_status": "VERIFIED",
      "detected_fields": {"income": 100000.0},
      "confidence": 0.88
    }
  ],
  "model_signals": [
    {
      "model_name": "XGBoost-CreditRisk",
      "model_version": "v1.0.0",
      "status": "EXPERIMENTAL",
      "score": 0.6,
      "confidence": 0.82,
      "reason_codes": ["HIGH_DEBT_TO_INCOME_RATIO"],
      "disclaimer": "EXPERIMENTAL BENCHMARK MODEL. Non-authoritative."
    }
  ],
  "ai_explanation": "UNDERWRITING EVALUATION SUMMARY (RISK_EXPLANATION):\n1. FACTS: Verified monthly income is ₹1,00,000.00 with monthly expenses of ₹40,000.00.\n2. CALCULATIONS: A ₹5,00,000 loan over 3 years @ 12.5% yields a monthly EMI of ₹16,726.81 (New DTI: 56.73%).\n3. MODEL SIGNAL: Credit Risk Model score is 0.6 (Status: EXPERIMENTAL, Reasons: ['HIGH_DEBT_TO_INCOME_RATIO']).\n4. POLICY EVIDENCE: Policy requires senior approval when DTI > 50%.\n5. DOCUMENT EVIDENCE: Verified salary document OCR snippet: 'Verified salary document sample text...'\n6. AI INFERENCE: The applicant has liquid reserves but high proposed DTI burden requires banker discretion.",
  "recommended_review_items": [
    "Verify monthly income of ₹1,00,000.00 against uploaded salary slip.",
    "Review Debt-to-Income impact (56.73%).",
    "Confirm senior credit committee authorization if DTI exceeds policy threshold."
  ],
  "requires_human_review": true
}
```
