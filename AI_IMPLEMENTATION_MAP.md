# AI Subsystem Architecture & Implementation Map - AgentTrust OS

**Author**: Member 3 (AI/ML/LLM/Agent Intelligence Subsystem Engineer)  
**Date**: August 25, 2026  

This document maps every AI subsystem component from its current state to its target production architecture, showing the exact model/technology, input data, output signals, and backend interface contracts.

---

## Architecture Flow Map

```text
Existing Component
        ↓
What It Should Become
        ↓
Actual Model / Technology
        ↓
Input Format
        ↓
Output Format
        ↓
Backend Contract Interface
```

---

## Detailed Component Maps

### 1. Document OCR Engine

```text
ai/app/perception/ocr_engine.py (Mock string decoder)
        ↓
Real High-Accuracy OCR Text & Line Bounding Box Extractor
        ↓
PaddleOCR v4 / Tesseract OCR 5.0
        ↓
Input: raw document file_bytes (PDF, PNG, JPEG)
        ↓
Output: List[OCRLine(text="...", confidence=0.98, bbox=[x1, y1, x2, y2])]
        ↓
Backend Contract: DocumentIntelligenceResult (ai/app/schemas/contracts/document.py)
```

---

### 2. Document Layout Detection

```text
ai/app/perception/layout.py (Mock bounding boxes)
        ↓
Real Document Layout & Structure Object Detector
        ↓
Ultralytics YOLOv8x-DocLayout / LayoutLMv3
        ↓
Input: document page image (PIL Image / numpy array)
        ↓
Output: List[LayoutElement(type="table"|"signature"|"stamp", bbox=[...], confidence=0.95)]
        ↓
Backend Contract: DocumentLayoutAnalysisDTO (ai/app/schemas/contracts/document.py)
```

---

### 3. Credit Risk Prediction ML

```text
ai/app/ml/risk_model.py (Mock linear logit formula)
        ↓
Real Gradient Boosted Credit Risk Model with SHAP Attributions
        ↓
XGBoost Classifier (trained model artifact: ai/models/xgb_risk_v1.json)
        ↓
Input: Dict[str, Any] (dti_ratio, past_delinquencies, savings_to_debt_ratio, credit_score)
        ↓
Output: RiskPredictionSignal(score=740, pd=0.03, risk_level="low", attributions=[...])
        ↓
Backend Contract: RiskAssessmentDTO (ai/app/schemas/contracts/risk.py)
```

---

### 4. Fraud Pattern Classification ML

```text
ai/app/ml/fraud_model.py (Mock velocity if/else rules)
        ↓
Real Gradient Boosted Fraud & Velocity Classifier
        ↓
LightGBM Classifier (trained model artifact: ai/models/lgbm_fraud_v1.txt)
        ↓
Input: Dict[str, Any] (failed_login_attempts, device_id_changed, ip_geo_distance_km)
        ↓
Output: FraudClassificationSignal(fraud_score=0.85, fraud_type="velocity_spike", severity="high")
        ↓
Backend Contract: FraudSignalDTO (ai/app/schemas/contracts/fraud.py)
```

---

### 5. Vector Embeddings & RAG Storage

```text
ai/app/providers/embedding.py (Mock sine wave math) & ai/app/rag/indexer.py (In-memory dict)
        ↓
Real Semantic Vector Embedding & Persistent Multi-Tenant Vector Database
        ↓
sentence-transformers/all-MiniLM-L6-v2 + ChromaDB / PGVector / FAISS
        ↓
Input: Document chunk text + Metadata (organization_id, user_id, document_id)
        ↓
Output: 384-dimensional dense vector embeddings & persistent HNSW index search
        ↓
Backend Contract: RAGSearchResultDTO (ai/app/schemas/contracts/rag.py)
```

---

### 6. LLM Gateway & Deterministic Financial Twin

```text
ai/app/gateway/gateway.py & ai/app/agents/financial_intelligence.py
        ↓
Unified Guarded AI Gateway + Pure Backend FinancialEngine
        ↓
Google Gemini 1.5 Flash / OpenAI GPT-4o-mini + Pure Python FinancialEngine (Decimal)
        ↓
Input: AIExecutionRequest (query, task, role, language, context)
        ↓
Output: AIExecutionResponse (explanation, exact figures retention, decision, evidence, audit)
        ↓
Backend Contract: AIExecutionResponseDTO (ai/app/schemas/contracts/ai_execution.py)
```

---

### 7. Agent Intelligence & Governance

```text
ai/app/agents/agent_intelligence.py
        ↓
9-Stage Agent Action Evaluation & Governance Pipeline
        ↓
AgentIntelligenceService (Identity -> Permission -> Risk -> Policy -> Recommendation)
        ↓
Input: AgentActionLog (agent_id, action, resource, parameters, context)
        ↓
Output: AgentDecisionRecommendation (decision: ALLOW | HOLD | BLOCK | HUMAN_REVIEW, explanation)
        ↓
Backend Contract: AgentEvaluationResultDTO (ai/app/schemas/contracts/agent.py)
```
