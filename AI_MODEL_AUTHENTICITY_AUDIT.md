# AgentTrust AI Subsystem — Model & Runtime Authenticity Audit

**Author**: Member 3 (Lead AI/ML/LLM/Agent Intelligence Lead)  
**Date**: August 26, 2026  
**Scope**: Technical Model Artifact, Perception, ML, RAG, and LLM Authenticity Investigation

---

## 1. Ultralytics YOLO Layout Model Authenticity Audit

- **Artifact Path**: `models/yolov8n.pt`
- **Architecture**: Ultralytics YOLOv8 Nano (`yolov8n`)
- **Training Dataset**: General-purpose COCO dataset (80 object classes: person, car, dog, etc.)
- **Authenticity Determination**:
  - The running model `models/yolov8n.pt` is a **generic pretrained COCO object detection model**.
  - It is **NOT** a fine-tuned, domain-specific document-layout model trained on financial documents (salary slips, bank statements, tax forms).
  - It cannot natively detect specialized document elements such as `Header`, `Table`, `Logo`, `Stamp`, or `Signature`.
- **Official Classification**:
  ```
  YOLO RUNTIME = LIVE_VERIFIED
  DOCUMENT-LAYOUT MODEL = NOT_PRODUCTION_VALIDATED
  ```

---

## 2. PaddleOCR Adapter Audit

- **Package Version**: `paddleocr` v2.7+ (with `pytesseract` fallback wrapper)
- **Execution Status**: **`LIVE_VERIFIED`**
- **Runtime Audit**:
  - Image preprocessing applies deskewing, contrast adjustment, and noise reduction.
  - Text line extraction runs actual inference on input image bytes.
  - Extracts text line strings, bounding box coordinates `[x_min, y_min, x_max, y_max]`, and individual line confidence scores (e.g. `0.88`).
  - Executed cleanly during live end-to-end smoke testing (`POST /ai/banker/underwriting`).

---

## 3. Financial ML Models Authenticity Audit (XGBoost / LightGBM / Isolation Forest)

- **XGBoost Credit Risk Architecture**:
  - Runtime Implementation: `XGBoostCreditRiskArchitecture` ([`ai/app/ml/risk_engine.py`](file:///d:/Agenttrust-os-/ai/app/ml/risk_engine.py))
  - Status: **`EXPERIMENTAL / SIMULATION`**
  - Finding: Training infrastructure (Phase 2B) is fully implemented. Public dataset benchmark metrics (UCI Credit Card ROC-AUC = 0.78) are unverified locally because datasets are not committed. In production assistant runtime, signals are generated via heuristic adapters and tagged `status = "EXPERIMENTAL"`.
- **LightGBM Fraud Architecture**:
  - Runtime Implementation: `LightGBMFraudArchitecture` ([`ai/app/ml/fraud_engine.py`](file:///d:/Agenttrust-os-/ai/app/ml/fraud_engine.py))
  - Status: **`EXPERIMENTAL / SIMULATION`**
  - Finding: Volatility checks evaluate transaction features and explicitly emit `status = "EXPERIMENTAL"`.
- **Isolation Forest Anomaly Architecture**:
  - Runtime Implementation: `IsolationForestAnomalyArchitecture` ([`ai/app/ml/anomaly_engine.py`](file:///d:/Agenttrust-os-/ai/app/ml/anomaly_engine.py))
  - Status: **`EXPERIMENTAL / SIMULATION`**

---

## 4. Permission-Aware RAG Infrastructure Audit

- **Embedding Model**: Local SentenceTransformers / `all-MiniLM-L6-v2` (384 dimensions)
- **Vector Store Implementation**: `PgVectorStore` ([`ai/app/rag/vector_store.py`](file:///d:/Agenttrust-os-/ai/app/rag/vector_store.py))
- **pgvector Live Connection Status**: **`BLOCKED`**
  - `PGVECTOR_HOST` environment variable is unconfigured locally.
  - The vector store cleanly falls back to JSON fixture search (`data/vector_store_chunks.json`) in development/test runner mode.
- **Classification**:
  ```
  RAG SECURITY & SEARCH = CODE_VERIFIED
  LIVE POSTGRESQL/PGVECTOR = BLOCKED
  ```

---

## 5. LLM Gateway & Provider Runtime Audit

- **Configured Default**: Provider `gemini`, Model `gemini-1.5-flash`
- **Execution Path**: Routed through `AIGateway.execute()` ([`ai/app/gateway/ai_gateway.py`](file:///d:/Agenttrust-os-/ai/app/gateway/ai_gateway.py)).
- **Fallback Chain Audit**:
  - When external LLM API keys are unconfigured on the local system, `AIGateway` cleanly executes a structured, deterministic fallback narrative engine.
  - Deterministic fallbacks clearly identify facts and calculations without pretending to be a live LLM model.
- **Classification**: **`CODE_VERIFIED`**

---

## 6. Financial Data & Environment Isolation Audit

- **Production Isolation**: Under `ENVIRONMENT=production` or `APP_ENV=production`, demo financial defaults (`₹1,00,000` income) are **STRICTLY BLOCKED** for all user IDs.
- **Backend Service Failure Handling**: If Member 1 backend HTTP service is unreachable in production, `FinancialDataProviderAdapter` strictly raises `FINANCIAL_DATA_UNAVAILABLE` with `requires_human_review = True`. Zero fabricated numbers are returned.
