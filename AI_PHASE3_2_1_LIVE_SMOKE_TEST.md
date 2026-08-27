# Phase 3.2.1 — Live End-to-End Smoke Test Report

**Author**: Member 3 (Lead AI/ML/LLM/Agent Intelligence Lead)  
**Date**: August 25, 2026  
**Scope**: Empirical Live Smoke Test Execution against FastAPI Assistant Service

---

## Executive Summary Results

```
TOTAL TESTS EXECUTED: 12
PASS: 8 | FAIL: 2 | BLOCKED: 2
```

> [!NOTE]
> Empirical runtime smoke testing was conducted against the active ASGI FastAPI engine (`POST /ai/assistant/query`). Per explicit instructions, no production code was modified to conceal failures or force artificial passes.

---

## Live Smoke Test Matrix

| Test ID | Test Name | Target Intent / Action | Status | Empirical Finding & Details |
| :---: | :--- | :--- | :---: | :--- |
| **TEST 1** | **Real User Query (English)** | `LOAN_AFFORDABILITY` | **PASS** | HTTP 200. `request_id`: `ast_req_8796df5b82`. `intent`: `LOAN_AFFORDABILITY`, `language`: `en`. Deterministic EMI calculated as `₹16,726.81` for `₹5,00,000.00` loan. |
| **TEST 2** | **Hindi Query Processing** | `LOAN_AFFORDABILITY` | **PASS** | HTTP 200. `language`: `hi`. Devanagari text correctly classified and Hindi response generated (`तथ्यों के आधार पर: आय ₹1,00,000.00...`). |
| **TEST 3** | **Hinglish Query Processing** | `LOAN_AFFORDABILITY` | **PASS** | HTTP 200. `language`: `hinglish`. Response generated in natural Hinglish (`Aapki income ₹1,00,000.00 ke anusar ₹16,726.81 EMI afford karna...`). |
| **TEST 4** | **Repayment Query** | `REPAYMENT_QUERY` | **PASS** | HTTP 200. Authoritative repayment amount `₹18,500.00` fetched from deterministic calculation engine. Zero LLM arithmetic. |
| **TEST 5** | **Unauthorized Data Shield** | Cross-User Access Guard | **PASS** | HTTP 200. User 101 requesting User 202's data (`target_user_id=202`). Intercepted by authorization shield, returned `ACCESS_DENIED`, `requires_human_review = True`. |
| **TEST 6** | **Organization Isolation** | Multi-Tenant Org Guard | **PASS** | HTTP 200. Request with empty/invalid `organization_id` returned `ACCESS_DENIED`, `requires_human_review = True`. |
| **TEST 7** | **Financial Action Shield** | Action Interception Guard | **FAIL** | HTTP 200. `"Approve this loan."` and `"Transfer ₹50,000."` were successfully blocked (`requires_human_review = True`). However, `"Change my repayment schedule."` matched `REPAYMENT_QUERY` intent rather than triggering action shield. |
| **TEST 8** | **Missing Data Protection** | Missing Service Guard | **FAIL** | When tested under unconfigured backend service, environment settings allowed fallback default figures rather than strictly raising `FINANCIAL_DATA_UNAVAILABLE`. |
| **TEST 9** | **LLM Provider Resilience** | Gateway Execution | **PASS** | HTTP 200. Request executed through `AIGateway` fallback pipeline cleanly. |
| **TEST 10** | **PostgreSQL + pgvector RAG** | Vector Database RAG | **BLOCKED** | `PGVECTOR_HOST` unconfigured on local environment. Live PostgreSQL similarity search test marked BLOCKED. |
| **TEST 11** | **Response Integrity** | Schema Validation | **PASS** | All required response keys (`request_id`, `answer`, `language`, `intent`, `facts`, `calculations`, `risk_signals`, `sources`, `confidence`, `requires_human_review`) present and valid. |
| **TEST 12** | **Logging & PII Redaction** | Observability Audit | **PASS** | Log outputs audited. Zero passwords, tokens, Aadhaar, PAN, or unredacted credentials exposed in stdout/stderr. |

---

## Detailed Test Logs & Payload Traces

### Test 1 — Real User Query (English)
- **Endpoint**: `POST /ai/assistant/query`
- **Request Payload**:
  ```json
  {
    "user_id": 101,
    "organization_id": "org_A",
    "role": "USER",
    "language": "en",
    "message": "Can I afford a ₹5 lakh loan?"
  }
  ```
- **Response Status**: `200 OK`
- **Response Payload**:
  ```json
  {
    "request_id": "ast_req_8796df5b82",
    "answer": "Based on financial facts: Calculated EMI of ₹16,726.81 for a ₹5,00,000.00 loan exceeds your maximum allowed buffer of ₹10,000.00.\nAssessment: This loan is currently unaffordable based on your cash flow.",
    "language": "en",
    "intent": "LOAN_AFFORDABILITY",
    "facts": [
      {"label": "Monthly Income", "value": "₹1,00,000.00", "source": "Member 1 Authoritative Financial API"},
      {"label": "Monthly Expenses", "value": "₹40,000.00", "source": "Member 1 Authoritative Financial API"}
    ],
    "calculations": [
      {"label": "Requested Loan Principal", "value": "₹5,00,000.00", "formula": "Deterministic Financial Engine"},
      {"label": "Calculated Monthly EMI", "value": "₹16,726.81", "formula": "Deterministic Financial Engine"},
      {"label": "Max Allowed Monthly EMI", "value": "₹10,000.00", "formula": "Deterministic Financial Engine"},
      {"label": "New Debt-To-Income (DTI)", "value": "56.73%", "formula": "Deterministic Financial Engine"},
      {"label": "Remaining Disposable Cash Flow", "value": "₹43,273.19", "formula": "Deterministic Financial Engine"}
    ],
    "risk_signals": [
      {"model_name": "XGBoost-CreditRisk", "score": 0.6, "status": "EXPERIMENTAL", "reason_codes": ["HIGH_DEBT_TO_INCOME_RATIO"]}
    ],
    "sources": [],
    "confidence": 0.95,
    "requires_human_review": false,
    "model_metadata": {"assistant_version": "v1.0.0", "organization_id": "org_A"}
  }
  ```

---

### Test 5 — Cross-User Security Guard
- **Request Payload**:
  ```json
  {
    "user_id": 101,
    "target_user_id": 202,
    "organization_id": "org_A",
    "role": "USER",
    "message": "Show financial profile for user 202"
  }
  ```
- **Response**:
  ```json
  {
    "request_id": "ast_req_5382a17f22",
    "answer": "ACCESS_DENIED: User 101 cannot access private financial data of User 202.",
    "language": "en",
    "intent": "UNAUTHORIZED_ACCESS",
    "requires_human_review": true
  }
  ```

---

## Remaining Blockers

1. **PostgreSQL pgvector Host**: `PGVECTOR_HOST` is unconfigured locally (`BLOCKED`).
2. **Action Shield Regex Pattern**: `"Change my repayment schedule."` needs pattern matching refinement for the multi-word action verb phrase.
3. **Environment Config Guard**: Production mode environment setting requires explicit instantiation guard when backend HTTP client is unreachable.
