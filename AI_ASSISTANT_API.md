# Financial Intelligence Assistant API Contract - AgentTrust OS

**Author**: Member 3 (AI/ML/LLM/Agent Intelligence Subsystem Lead)  
**Date**: August 25, 2026  
**Scope**: OpenAPI Endpoint Specification for Frontend Integration (Member 2)

---

## Endpoint Specification

### `POST /ai/assistant/query`

#### Request Body Schema ([`AssistantQueryRequest`](file:///d:/Agenttrust-os-/ai/app/schemas/assistant.py))
```json
{
  "user_id": 101,
  "target_user_id": null,
  "organization_id": "org_A",
  "role": "USER",
  "language": "hi",
  "message": "Mera 5 lakh loan afford hoga?"
}
```

#### Response Body Schema ([`AssistantQueryResponse`](file:///d:/Agenttrust-os-/ai/app/schemas/assistant.py))
```json
{
  "request_id": "ast_req_eea09bd4f1",
  "answer": "Aapki monthly income ₹80,000.00 aur expenses ₹25,000.00 hain. Calculated EMI: ₹5,00,000.00 loan ke liye 3 sal ki EMI ₹16,726.81 hogi. Result: Haan, aap ₹5,00,000.00 ka loan afford kar sakte hain.",
  "language": "hinglish",
  "intent": "LOAN_AFFORDABILITY",
  "facts": [
    {"label": "Monthly Income", "value": "₹80,000.00", "source": "Member 1 Authoritative Financial API"},
    {"label": "Monthly Expenses", "value": "₹25,000.00", "source": "Member 1 Authoritative Financial API"}
  ],
  "calculations": [
    {"label": "Calculated Monthly EMI", "value": "₹16,726.81", "formula": "Deterministic Financial Engine"},
    {"label": "Max Allowed Monthly EMI", "value": "₹15,000.00", "formula": "Deterministic Financial Engine"},
    {"label": "New Debt-To-Income (DTI)", "value": "52.16%", "formula": "Deterministic Financial Engine"}
  ],
  "risk_signals": [
    {
      "model_name": "XGBoost-CreditRisk",
      "score": 0.35,
      "status": "EXPERIMENTAL",
      "reason_codes": ["STABLE_REPAYMENT_PROFILE"]
    }
  ],
  "sources": [],
  "confidence": 0.95,
  "requires_human_review": false,
  "model_metadata": {
    "assistant_version": "v1.0.0",
    "organization_id": "org_A"
  }
}
```
