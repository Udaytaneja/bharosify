# AI Model Registry & Artifact Status - AgentTrust OS

**Author**: Member 3 (AI/ML/LLM/Agent Intelligence Subsystem Lead)  
**Date**: August 25, 2026  
**Scope**: Model Artifact Inventory & Lifecycle Status

---

## Model Inventory & Lifecycle Status

| Model Name | Model Type | Provider | Artifact Path | Status | Loaded Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **PaddleOCR-v4** | OCR Text & Line Bounding Box | `paddleocr` | `ch_PP-OCRv4_rec` | **IMPLEMENTED / CONFIGURED** *(Runtime fallback ready)* | Singleton Lazy Loaded |
| **YOLOv8-DocLayout** | Document Layout Object Detection | `ultralytics` | `YOLO_MODEL_PATH` | **IMPLEMENTED / CONFIG-READY** *(Awaiting `.pt` artifact)* | Singleton Lazy Loaded |
| **XGBoost Credit Risk** | Credit Risk Prediction ML | `xgboost` | `xgb_risk_v1.json` | **PHASE 2B TARGET** | Pending Phase 2B |
| **LightGBM Fraud Pattern** | Fraud & Anomaly Classification | `lightgbm` | `lgbm_fraud_v1.txt` | **PHASE 2B TARGET** | Pending Phase 2B |
| **Sentence-Transformers** | 384d Dense Vector Embeddings | `sentence-transformers` | `all-MiniLM-L6-v2` | **PHASE 2C TARGET** | Pending Phase 2C |

---

## Status Classification Key

- **IMPLEMENTED**: Code adapters, lifecycle hooks, and tests are 100% complete.
- **CONFIGURED**: Environment settings and configuration parameters exist in `AISettings`.
- **MODEL-READY**: Model artifact file is loaded and active in memory.
- **MOCK**: Pure simulation (Deprecated in Phase 2A).
- **NOT AVAILABLE**: Model artifact path is unconfigured or file is missing (system handles gracefully with structured status `MODEL_UNAVAILABLE`).
