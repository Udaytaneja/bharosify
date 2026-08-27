# AgentTrust OS — AI/ML Architecture Audit & Blueprint

**Role**: Lead AI/ML Architect (Member 3)  
**Date**: August 2026  
**Status**: Completed Architectural Audit  
**Scope**: Complete AI/ML/LLM/Agent Intelligence Layer  

---

## Executive Summary

This document establishes the comprehensive technical audit, safety governance, data contracts, and implementation blueprint for the **AI/ML/LLM/Agent Intelligence Layer** of **AgentTrust OS**. 

As Member 3 (Lead AI/ML Architect), this audit respects all structural boundaries:
- **Authoritative Backend**: Member 1's backend remains the single source of truth for authentication, user profiles, financial ledgers, applications, underwriting decisions, loan balances, repayments, and governance permissions.
- **Frontend Contract**: Member 2's frontend remains unchanged and communicates exclusively via the existing `/api/v1` REST contract.
- **Core Principle of AI Safety**: AI models generate predictions, risk signals, anomaly scores, OCR extraction, natural language recommendations, and explainability attributions. **AI services NEVER directly execute money transfers, approve/reject loans, alter user roles, or bypass policy controls.** All AI output recommendations pass through deterministic backend validation engines and human-in-the-loop (HITL) banker workflows.

---

## A. Current Architecture

### 1. High-Level System Architecture
```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│                                   FRONTEND                                       │
│                Vite + React + TypeScript (User & Banker Workspaces)              │
└────────────────────────────────────────┬─────────────────────────────────────────┘
                                         │  HTTP / REST (`/api/v1`)
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                                  BACKEND API                                     │
│            FastAPI + Pydantic v2 + SQLAlchemy (Async) + JWT Authentication        │
└──────────────────────┬────────────────────────────────────┬──────────────────────┘
                       │                                    │
                       ▼                                    ▼
┌───────────────────────────────┐                  ┌───────────────────────────────┐
│       AUTHORITATIVE DB        │                  │         AI ENGINE (ai/)       │
│  PostgreSQL / AsyncPG Ledger  │                  │ Member 3 Intelligence Engine │
│ (Users, Loans, Audit Logs)    │                  │  (Gateway, RAG, Models, XAI)  │
└───────────────────────────────┘                  └───────────────────────────────┘
```

### 2. Subsystem Ownership & Boundaries
* **Frontend (`frontend/`)**: React 18, Vite, TypeScript, TailwindCSS, Axios API client with token auto-refresh. Supports dual roles (`user` and `banker`) and bilingual internationalization (`en` and `hi`).
* **Backend (`backend/app/`)**: FastAPI application, PostgreSQL ORM models (`SQLAlchemy`), Pydantic v2 schemas, JWT security (`pwdlib` Argon2), and REST routers under `/api/v1`.
* **Contracts (`contracts/`)**: Version-controlled markdown contracts (`api.md`, `enums.md`, `schemas.md`) standardizing shared schemas (`AIRequest`, `AIResponse`, `RiskAssessment`, `FraudSignal`, `Underwriting`, etc.).
* **AI Subsystem (`ai/`)**: Designated root directory for Member 3's intelligent services, models, pipelines, and evaluation frameworks.

---

## B. Existing AI Capabilities

### 1. API Endpoints (`backend/app/api/ai.py`)
The backend exposes four dedicated REST routes under `/api/v1/ai`:
* `POST /api/v1/ai/chat` (Accessible by User & Banker): General financial query assistant and localized advice.
* `POST /api/v1/ai/scenario` (Accessible by User & Banker): Financial simulation (e.g., impact of loan repayment on cashflow).
* `POST /api/v1/ai/risk-analysis` (Banker Only): Risk factor assessment and evidence synthesis.
* `POST /api/v1/ai/underwriting` (Banker Only): Loan application underwriting recommendation and confidence evaluation.

### 2. Current Implementation State
* Currently, `backend/app/api/ai.py` delegates calls to `handle_ai_request()` in `backend/app/services/system_service.py`.
* `handle_ai_request()` writes an audit record to `AuditEvent` table and returns a static mock response string:
  ```python
  AIResponse(
      request_id=payload.request_id,
      response=f"[AI Engine Ready] Processed task '{task_type}' for input: {payload.input}",
      reasoning_summary=f"Context verified for user {current_user.id} ({current_user.role}).",
      evidence=["Verified profile data", "Historical transaction stability"],
      recommendation="approve" if current_user.role == "banker" else "review",
      requires_human_review=False
  )
  ```
* **Audit Verdict**: The AI pipeline is currently a static stub. No model routing, vector retrieval, OCR processing, prompt engineering, or risk scoring algorithms are active.

---

## C. Existing Backend Contracts

### 1. Core AI Data Schemas (`contracts/schemas.md` & `backend/app/schemas/system.py`)

#### `AIRequest` Schema
```json
{
  "request_id": "string",
  "task": "chat | scenario | risk_analysis | underwriting",
  "input": "string",
  "language": "en | hi",
  "context": "object (optional key-value payload)"
}
```

#### `AIResponse` Schema
```json
{
  "request_id": "string",
  "response": "string",
  "confidence": "number (0.00 to 1.00)",
  "reasoning_summary": "string",
  "evidence": ["array of string claims/citations"],
  "recommendation": "approve | review | reject | escalate",
  "requires_human_review": "boolean"
}
```

### 2. Relevant Financial & Risk Schemas
* `RiskAssessment`: `score` (0-1000), `level` (`low`, `medium`, `high`, `critical`), `factors` (JSON), `evidence` (JSON), `recommendation`, `confidence`.
* `FraudSignal`: `transaction_id`, `type`, `severity`, `score`, `evidence` (JSON), `status`.
* `Underwriting`: `application_id`, `risk_score`, `risk_level`, `factors` (JSON), `evidence` (JSON), `recommendation`, `confidence`, `human_review_required`, `decision`.
* `TrustProfile`: `score` (300-850), `level`, `change`, `factors` (list of `TrustFactor`).

---

## D. Missing AI Infrastructure

1. **AI Provider Gateway & Fallback Layer**: No abstraction layer for LLM API providers (Google Gemini, OpenAI, Anthropic) or local model endpoints (Ollama/vLLM).
2. **Model Router**: No dynamic task router to select cost-optimal models based on latency budget, task type, and user tier.
3. **Document Intelligence & OCR Engine**: Missing document processing pipeline for bank statements, salary slips, tax forms (ITR), and ID proofs.
4. **Financial Digital Twin & Signal Engines**: Missing computational ML models for transaction anomaly detection, financial health scoring, cashflow volatility calculation, and credit risk ensembling.
5. **RAG & Vector Grounding Engine**: Missing vector database integration (e.g., Qdrant / PGVector), embedding generation pipeline, and semantic document retrieval.
6. **AI Safety & PII Redaction Guardrails**: Missing sanitization layer to strip personally identifiable information (PII) like Aadhaar numbers, PAN, and full account numbers before querying external LLMs.
7. **Explainability (XAI) Engine**: Missing SHAP / feature attribution generator and evidence grounding binder.
8. **Agent Governance & Policy Enforcer**: Missing runtime environment to evaluate agent action safety, verify permission boundaries, and trigger Human-in-the-loop (HITL) alerts.

---

## E. Integration Risks

1. **HTTP Request Timeouts**: LLM calls and complex RAG queries may take 2–10 seconds. Direct synchronous invocation inside FastAPI request handlers could block client requests or exceed server timeout thresholds.
2. **Database Connection Strain**: Unbounded async tasks spawned during vector retrieval or model inference could exhaust SQLAlchemy connection pools.
3. **Payload Structure Discrepancies**: Free-form LLM JSON outputs might violate strict Pydantic `AIResponse` validation, raising unhandled 500 errors.
4. **Bilingual Semantic Drift**: Translating financial terminology between English and Hindi (`hi`) could lead to altered prompt contexts or misinterpreted loan intent.

---

## F. Security Risks

1. **Prompt Injection & Persona Jailbreaks**: Attackers craft inputs to overwrite system instructions and manipulate risk scores or loan recommendations.
2. **PII Data Leakage to Third-Party APIs**: Sending raw user documents, names, tax details, or transaction histories to external LLM providers violates enterprise privacy policies and regulatory frameworks (e.g., RBI guidelines, GDPR/DPDP).
3. **API Key Exposure**: Accidentally reading or exposing `AI_API_KEY` to frontend bundle configurations.
4. **Agent Escalation of Privilege**: An ungrounded AI agent generating automated API actions beyond its granted role scope (`user` executing `banker` functions).

---

## G. Data-Flow Problems

1. **Lack of Asynchronous Background Task Queue**: Uploaded PDFs and large transaction files cannot be parsed synchronously inside standard FastAPI POST endpoints without blocking HTTP threads.
2. **Redundant Database Queries**: Repeatedly querying transaction histories and profiles across multiple AI sub-tasks without an in-memory caching tier (e.g., Redis).
3. **Raw vs. Sanitized Context Loss**: Stripping context for PII protection without maintaining a secure mapping key prevents re-linking evidence to user records during banker review.

---

## H. Dependency Risks

1. **Missing Core Libraries in Workspace Python Environment**: Running tests currently yields `ModuleNotFoundError: No module named 'pydantic_settings'`, indicating that dependencies listed in `backend/requirements.txt` are not active in the default system environment.
2. **Heavyweight Dependencies**: Introducing PyTorch, OpenCV, or native C++ OCR engines directly into the lightweight web container inflates image size and memory footprint.
3. **Third-Party API Rate Limits**: Reliance on a single LLM API provider creates a single point of failure during provider outages or quota exhaustion.

---

## I. Recommended AI Architecture

To address all missing infrastructure while adhering strictly to core constraints, Member 3 proposes the following **Modular Layered AI Architecture**:

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   FASTAPI API ROUTERS                                       │
│                            (`backend/app/api/ai.py`)                                        │
└──────────────────────────────────────────┬──────────────────────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 AI ENGINE ENTRY POINT                                       │
│                                  `ai/engine.py`                                             │
└─────────┬────────────────────────────────┬──────────────────────────────────────┬───────────┘
          │                                │                                      │
          ▼                                ▼                                      ▼
┌──────────────────┐           ┌───────────────────────┐              ┌──────────────────────┐
│  SAFETY & PII    │           │     MODEL ROUTER      │              │ DOCUMENT INTEL / OCR │
│  GUARDRAILS      │           │   `ai/router/`        │              │  `ai/perception/`    │
│ `ai/safety/`     │           └───────────┬───────────┘              └──────────────────────┘
└──────────────────┘                       │
                                           ▼
                       ┌──────────────────────────────────────┐
                       │          AI GATEWAY LAYER            │
                       │          `ai/gateway/`               │
                       │ (Gemini, OpenAI, Local Fallback)     │
                       └──────────────────┬───────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                             SPECIALIZED INTELLIGENCE ENGINES                                │
├─────────────────────────┬──────────────────────────┬──────────────────────────┬─────────────┤
│  FINANCIAL DIGITAL TWIN │    RISK & FRAUD ML       │  UNDERWRITING ADVISOR    │ AGENT GOV.  │
│  `ai/models/health.py`  │ `ai/models/risk_fraud.py`│ `ai/models/underwrite.py`│ `ai/agents/`│
└─────────────────────────┴──────────────────────────┴──────────────────────────┴─────────────┤
                                          │                                                   │
                                          ▼                                                   ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                              EXPLAINABILITY & ATTRIBUTION (XAI)                             │
│                                  `ai/explainability/`                                       │
└─────────────────────────────────────────┬───────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                             OBSERVABILITY & TOKEN AUDITING                                  │
│                                 `ai/observability/`                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## J. Recommended Directory Structure

```text
ai/
├── __init__.py
├── engine.py                   # Main entry point orchestrator for Member 1 backend
├── gateway/                    # Multi-provider LLM abstraction
│   ├── __init__.py
│   ├── base.py                 # Abstract Base Class for Providers
│   ├── gemini.py               # Google Gemini Adapter
│   ├── openai.py               # OpenAI Adapter
│   └── router.py               # Fallback & Load Balancer
├── router/                     # Task Routing & Model Selection
│   ├── __init__.py
│   └── task_router.py
├── perception/                 # Computer Vision & OCR Parsing
│   ├── __init__.py
│   ├── document_ocr.py         # Multi-format PDF / Image parser
│   └── statement_analyzer.py   # Bank statement extractor
├── rag/                        # RAG & Grounding Pipeline
│   ├── __init__.py
│   ├── embeddings.py           # Vector embedding generator
│   └── vector_store.py         # In-memory / PGVector indexer
├── models/                     # Deterministic & ML Signal Models
│   ├── __init__.py
│   ├── financial_twin.py       # Cashflow twin & health evaluator
│   ├── trust_engine.py         # Dynamic trust score calculator
│   ├── risk_fraud_engine.py    # Anomaly & fraud signal generator
│   └── underwriting_engine.py  # Credit risk ensemble
├── agents/                     # Agent Intelligence & Governance
│   ├── __init__.py
│   ├── runtime.py              # Agent behaviour sandbox
│   └── policy_enforcer.py      # RBAC permission boundary check
├── safety/                     # AI Safety & Guardrails
│   ├── __init__.py
│   ├── pii_sanitizer.py        # Masking Aadhaar, PAN, Account Nos
│   ├── prompt_guard.py         # Injection & jailbreak detection
│   └── bounded_decider.py      # Enforces Non-Authoritative rule
├── explainability/             # Explainable AI (XAI)
│   ├── __init__.py
│   ├── attribution.py          # SHAP-like feature scoring
│   └── reasoning_grounder.py   # Citation & evidence builder
├── observability/              # Telemetry & Cost Tracking
│   ├── __init__.py
│   ├── logger.py               # Audit logger
│   └── metrics.py              # Token meter & latency tracking
└── schemas/                    # Internal AI Pydantic Data Models
    ├── __init__.py
    └── internal.py
```

---

## K. Required APIs

Internal Python interfaces exported by `ai/engine.py` for consumption by `backend/app/api/ai.py` and service layers:

```python
async def process_chat(
    user_id: int, 
    role: str, 
    input_text: str, 
    language: str, 
    db_session: AsyncSession
) -> AIResponse: ...

async def process_scenario_simulation(
    user_id: int, 
    role: str, 
    input_text: str, 
    language: str, 
    context: dict, 
    db_session: AsyncSession
) -> AIResponse: ...

async def process_banker_risk_analysis(
    banker_id: int, 
    customer_id: int, 
    input_text: str, 
    db_session: AsyncSession
) -> AIResponse: ...

async def process_banker_underwriting(
    banker_id: int, 
    application_id: int, 
    input_text: str, 
    db_session: AsyncSession
) -> AIResponse: ...
```

---

## L. Required Schemas (`ai/schemas/internal.py`)

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class FeatureAttribution(BaseModel):
    feature_name: str
    weight: float
    direction: str  # "positive" | "negative" | "neutral"
    description: str

class MLRiskSignal(BaseModel):
    risk_score: int = Field(ge=0, le=1000)
    risk_level: str  # "low" | "medium" | "high" | "critical"
    confidence: float = Field(ge=0.0, le=1.0)
    attributions: List[FeatureAttribution]
    evidence_sources: List[str]
    suggested_recommendation: str  # "approve" | "review" | "reject" | "escalate"

class OCRDocumentResult(BaseModel):
    document_type: str  # "bank_statement" | "pay_slip" | "tax_return" | "id_proof"
    extracted_text: str
    structured_data: Dict[str, Any]
    confidence: float
```

---

## M. Required Model Interfaces (`ai/gateway/base.py`)

```python
from abc import ABC, abstractmethod
from pydantic import BaseModel

class LLMProviderResponse(BaseModel):
    text: str
    token_usage: dict
    finish_reason: str
    raw_response: Any

class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate_text(self, prompt: str, system_instruction: Optional[str] = None) -> LLMProviderResponse:
        pass

    @abstractmethod
    async def generate_structured(self, prompt: str, schema: type[BaseModel]) -> BaseModel:
        pass
```

---

## N. Required Environment Variables

Add the following environment configuration to `.env.example` and `backend/app/core/config.py`:

```ini
# AI Gateway Configuration
AI_API_KEY=your-api-key-here
AI_PROVIDER=gemini           # gemini | openai | local
AI_MODEL=gemini-1.5-flash    # gemini-1.5-flash | gemini-1.5-pro | gpt-4o-mini
AI_FALLBACK_PROVIDER=local   # local | none
AI_MAX_TOKENS=2048
AI_TEMPERATURE=0.2

# Document OCR Configuration
OCR_ENGINE=tesseract          # tesseract | easyocr | mock
OCR_MAX_FILE_SIZE_MB=10

# AI Safety & Guardrails
PII_REDACTION_ENABLED=true
PROMPT_INJECTION_SHIELD=true

# AI Telemetry
AI_TELEMETRY_ENABLED=true
```

---

## O. Testing Strategy

1. **Unit Tests (`ai/tests/unit/`)**:
   * Test PII sanitizer masking logic against test samples (PAN, Aadhaar, Account numbers).
   * Test prompt guard injection detection with adversarial inputs.
   * Test OCR document text extraction formats.
2. **Integration Tests (`ai/tests/integration/`)**:
   * Test gateway fallback when primary provider raises API error.
   * Test end-to-end integration between `backend/app/api/ai.py` and `ai/engine.py` using synthetic test database fixtures.
3. **Model Evaluation Tests (`ai/tests/evals/`)**:
   * Test output schema compliance (100% adherence to `AIResponse`).
   * Verify non-authoritative boundary checks (ensuring model recommendations never bypass deterministic backend rules).
   * Evaluate Hindi (`hi`) prompt translation accuracy.

---

## P. Observability Strategy

1. **Token & Cost Ledger**: Log token consumption per user, role, and task type in `AuditEvent` or dedicated log streams.
2. **Latency Tracking**: Track execution duration for OCR, RAG retrieval, LLM generation, and XAI attribution.
3. **Drift & Evaluation Monitoring**: Log model output confidence distributions to detect prompt decay or schema misalignment.

---

## Q. Deployment Strategy

1. **In-Process Python Module Deployment**: Execute `ai/` as an internal asynchronous library imported directly by FastAPI workers for zero network-hop latency.
2. **Worker Isolation**: Offload heavy OCR tasks and embedding generation to background workers (e.g. FastAPI `BackgroundTasks` or Redis Streams worker) to prevent API latency spikes.
3. **Stateless Scalability**: Ensure all AI modules are strictly stateless, delegating state storage to Postgres DB and Redis.

---

## R. Recommended Implementation Order

1. **Phase 1: AI Core Foundation & Safety Shield**
   * Setup directory structure under `ai/`.
   * Implement `ai/safety/pii_sanitizer.py` and `ai/safety/bounded_decider.py`.
   * Implement `ai/gateway/` provider abstraction with Gemini and fallback adapters.

2. **Phase 2: RAG & Financial Data Engines**
   * Implement `ai/perception/document_ocr.py` for bank statement and PDF parsing.
   * Implement `ai/models/financial_twin.py` (cashflow analysis & health score).
   * Implement `ai/models/trust_engine.py` (dynamic trust factors).

3. **Phase 3: Risk, Underwriting & XAI**
   * Implement `ai/models/risk_fraud_engine.py` (fraud signals & risk assessment).
   * Implement `ai/models/underwriting_engine.py` (banker underwriting synthesis).
   * Implement `ai/explainability/` (SHAP-style feature attributions).

4. **Phase 4: Agent Governance & Telemetry**
   * Implement `ai/agents/policy_enforcer.py` (permission sandbox).
   * Implement `ai/observability/` metrics & logging.
   * Wire `ai/engine.py` to `backend/app/api/ai.py` replacing static stubs.
