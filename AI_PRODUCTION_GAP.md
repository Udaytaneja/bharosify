# AI Subsystem Production Gap Analysis - AgentTrust OS

**Author**: Member 3 (AI/ML/LLM/Agent Intelligence Subsystem Engineer)  
**Date**: August 25, 2026  

This document ranks all identified production blockers into strict priority buckets:
- **P0**: Security, Correctness, & Real Model Inference Blockers
- **P1**: Required for MVP Readiness
- **P2**: Scale, Storage, & Performance Optimizations
- **P3**: Future Model & Pipeline Enhancements

---

## P0: Security, Correctness, & Model Inference Blockers (CRITICAL)

1. **Mock OCR Engine (`PaddleOCREngine`)**:
   - *Current Gap*: `PaddleOCREngine` decodes raw string bytes and returns mock lines + static bounding boxes.
   - *Production Impact*: Document processing fails to extract real text or line coordinates from uploaded PDFs/images.
   - *Action*: Wire real `paddleocr` / Tesseract OCR inference adapter.

2. **Mock YOLO Layout Analyzer (`YOLOLayoutAnalyzer`)**:
   - *Current Gap*: `YOLOLayoutAnalyzer` returns hardcoded `LayoutElement` bounding box coordinates.
   - *Production Impact*: Tables, logos, headers, stamps, and signatures are not visually detected in real document layouts.
   - *Action*: Integrate real `ultralytics` YOLOv8-DocLayout model inference engine.

3. **Rule-Based Risk ML & Fraud ML Models**:
   - *Current Gap*: `RiskPredictionModel` claims XGBoost but uses `logit = 2.5 - (dti * 3.5)...`. `FraudClassificationModel` claims LightGBM but uses `if failed_logins >= 3...` rules.
   - *Production Impact*: Credit scoring and fraud detection rely on hand-written heuristics rather than statistical machine learning weights.
   - *Action*: Implement trained model artifact loaders (`.joblib` / `.json`) for XGBoost and LightGBM inference.

4. **Pseudo Vector Embeddings (`VectorEmbeddingAdapter`)**:
   - *Current Gap*: `embed_text()` calculates `math.sin(seed + i)`.
   - *Production Impact*: Vector search similarity scores are pseudo-random math sine waves rather than semantic text similarity.
   - *Action*: Integrate real `sentence-transformers` (e.g. `all-MiniLM-L6-v2`) or Google `text-embedding-004` provider.

5. **In-Memory Vector Store Indexer (`VectorStoreIndexer`)**:
   - *Current Gap*: `VectorStoreIndexer` stores document chunks in a Python dictionary `self._chunks`.
   - *Production Impact*: Indexed RAG document chunks are lost whenever the server process restarts.
   - *Action*: Replace in-memory dictionary with persistent vector storage engine (ChromaDB / PGVector / Qdrant).

6. **Direct Backend ORM Coupling**:
   - *Current Gap*: `ai/app/ml/backend_integration.py` directly imports `backend.app.models...` ORM models (`RiskAssessment`, `FraudSignal`, `TrustFactor`).
   - *Production Impact*: Couples Member 3's AI subsystem to Member 1's backend DB models, creating circular import risks and breaking architectural modularity.
   - *Action*: Decouple imports using explicit Pydantic DTO Contract Adapters (`ai/app/schemas/contracts/`).

---

## P1: Required for MVP Readiness

1. **Asynchronous Heavy Inference Pipeline**:
   - *Current Gap*: Document OCR and ML prediction steps execute synchronously in the HTTP request thread.
   - *Production Impact*: Large PDF processing can block the FastAPI event loop under concurrent load.
   - *Action*: Implement async worker queues for heavy document perception tasks.

2. **Model Artifact Management & Versioning**:
   - *Current Gap*: Model artifacts (weights, scaler parameters) do not have a dedicated local directory or remote storage bucket loader.
   - *Action*: Create `ai/models/` artifact storage registry for XGBoost, LightGBM, and LayoutLM model files.

3. **HTTP Provider Client Standardization**:
   - *Current Gap*: `GeminiProvider` uses Python standard library `urllib.request`.
   - *Action*: Upgrade provider HTTP calls to non-blocking `httpx.AsyncClient` with connection pooling.

---

## P2: Scale, Storage, & Performance Optimizations

1. **Persistent FAISS / PGVector Vector Storage**:
   - *Target*: Scale vector storage to millions of chunks with metadata filtering index.
2. **Local Provider Support (Ollama / vLLM)**:
   - *Target*: Support zero-latency local fallback models (e.g., Llama-3-8B / Qwen-2.5) for air-gapped deployments.
3. **OpenTelemetry Distributed Tracing**:
   - *Target*: Export AI Gateway execution spans to Jaeger / Grafana Tempo.

---

## P3: Future Model & Pipeline Enhancements

1. **Fine-Tuned LayoutLMv3 Document Classifier**:
   - *Target*: Replace rule-based keyword document classification with multi-modal vision-language layout classification.
2. **DeBERTa-v3 Prompt Injection Model**:
   - *Target*: Replace regex prompt injection checks with fine-tuned DeBERTa-v3 classifier model.
3. **Image Error Level Analysis (ELA) Tampering Detection**:
   - *Target*: Add pixel-level image compression artifact analysis for altered document detection.
