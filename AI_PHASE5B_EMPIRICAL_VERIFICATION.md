# Phase 5B.1 — Document Layout Model Empirical Verification Report

**Author**: Member 3 (Lead AI/ML/LLM/Agent Intelligence Lead)  
**Date**: August 26, 2026  
**Scope**: Empirical Local Filesystem, Model Artifact, Metric Provenance & Integration Audit for Phase 5B

---

## Executive Verification Summary

```
DATASET PRESENT: NO (DATASET_NOT_PRESENT)
MODEL ARTIFACT PRESENT: NO (MODEL_ARTIFACT_NOT_PRESENT)
METRICS VERIFICATION STATUS: METRICS_NOT_EMPIRICALLY_VERIFIED
PRODUCTION INTEGRATION READINESS: INTEGRATION_REQUIRES_CONFIGURATION
MODEL REGISTRY STATUS: EXPERIMENTAL / CANDIDATE
PRODUCTION CODE CHANGED: 0
WORKSPACE TESTS PASSED: 196 PASSED / 3 SKIPPED (100% PASS RATE)
```

---

## 1. Dataset Empirical Verification

- **Dataset Actually Present?**: **`NO (DATASET_NOT_PRESENT)`**
- **Verified Dataset Size**: `0 pages` stored locally.
- **Audit Details**:
  - Inspection of local directories `data/raw/` and `data/processed/` shows that the full 80,863 page DocLayNet dataset images and raw JSON annotation files are not stored on the local disk (they remain gitignored and unpopulated in the local workspace).
  - Dataset metadata governance definitions exist in [`ai/app/ml/datasets/doclaynet_metadata.py`](file:///d:/Agenttrust-os-/ai/app/ml/datasets/doclaynet_metadata.py) with verified `CC-BY-4.0` license status.

---

## 2. Model Artifact Empirical Verification

- **Model Artifact Actually Present?**: **`NO (MODEL_ARTIFACT_NOT_PRESENT)`**
- **Target Path**: `artifacts/training/doc_layout/yolov8_doclayout_v1.pt`
- **Artifact SHA-256**: `NONE (FILE_NOT_FOUND)`
- **File Size**: `0 bytes`
- **Model Registry Status**: Registered in `ExperimentManifestManager` as **`EXPERIMENTAL`** / **`CANDIDATE`**.

---

## 3. Training Run & Metric Provenance Audit

- **Original Reported Metrics**:
  - `mAP@50`: `0.885`
  - `mAP@50-95`: `0.692`
  - `Precision`: `0.912`
  - `Recall`: `0.864`
  - `Inference Latency`: `14.2 ms`
- **Training Run Evidence**: **`METRICS_NOT_EMPIRICALLY_VERIFIED`**
- **Audit Finding**:
  - The reported metrics were generated during pipeline architecture dry-run manifest logging rather than actual CUDA training against the full 80,863 page DocLayNet corpus on local hardware.
  - No local `results.csv` or Ultralytics CUDA training log files exist on the filesystem.

---

## 4. Reproducibility & Hyperparameters

- **Seed**: `42`
- **Epochs**: `10` (configured default)
- **Batch Size**: `16`
- **Image Size**: `640`
- **Base Checkpoint**: `yolov8n.pt`
- **Training Module**: [`ai/app/ml/training/train_document_layout.py`](file:///d:/Agenttrust-os-/ai/app/ml/training/train_document_layout.py)
- **Reproducibility Rating**: Fully reproducible via `python -m ai.app.ml.training.train_document_layout` once raw dataset images are downloaded to `data/raw/`.

---

## 5. Independent Validation & Metric Discrepancy

- **Independent Measured Metrics**: **`METRICS_NOT_EMPIRICALLY_VERIFIED`**
- **Discrepancy Note**: Independent validation on held-out test splits could not be executed because raw image files and `.pt` model weights do not exist on the local disk.

---

## 6. Model Class Verification

- **Defined Model Classes**: 11 DocLayNet mapped layout classes:
  1. `CAPTION`
  2. `FOOTNOTE`
  3. `FORMULA`
  4. `LIST_ITEM`
  5. `PAGE_FOOTER`
  6. `PAGE_HEADER`
  7. `FIGURE`
  8. `SECTION_HEADER`
  9. `TABLE`
  10. `TEXT_BLOCK`
  11. `TITLE`
- **Class Index Mapping**: Verified 1-to-1 in [`DOCLAYNET_CLASS_MAPPING`](file:///d:/Agenttrust-os-/ai/app/ml/datasets/doclaynet_metadata.py). Zero index mismatches found.

---

## 7. Data Leakage Audit

- **Grouping Protection**: Implemented in `DocLayNetYOLOConverter.deterministic_split_documents()` using fixed `seed = 42`.
- **Grouping Rule**: Document pages sharing the same `document_id` are strictly grouped together, ensuring 0% document cross-contamination between train, val, and test splits.

---

## 8. Real Inference Test

- **Execution Finding**: Real inference on local test images could not be performed due to missing `.pt` weight files (`MODEL_ARTIFACT_NOT_PRESENT`).
- **Safety Handling**: Perception adapter (`YOLOLayoutAnalyzer`) cleanly returns `status = PerceptionStatus.MODEL_UNAVAILABLE` without fabricating hardcoded bounding boxes or fake detections.

---

## 9. Production Integration Readiness

- **Status**: **`INTEGRATION_REQUIRES_CONFIGURATION`**
- **Inspection**: In [`ai/app/perception/layout.py`](file:///d:/Agenttrust-os-/ai/app/perception/layout.py), `ai_settings.yolo_model_path` defaults to unconfigured/generic path.
- **Action Needed**: Set `yolo_model_path = "artifacts/training/doc_layout/yolov8_doclayout_v1.pt"` in environment configuration once model training completes.

---

## 10. Remaining Indian-Domain Gap

- **DocLayNet Limitation**: DocLayNet layout classes (`TABLE`, `TEXT_BLOCK`, `TITLE`) do **NOT** cover Indian bank statements (HDFC, ICICI, SBI), Aadhaar cards, PAN cards, or salary slips.
- **Domain Specification**: Custom domain fine-tuning based on [`docs/ai/INDIAN_DOCUMENT_ANNOTATION_SPEC.md`](file:///d:/Agenttrust-os-/docs/ai/INDIAN_DOCUMENT_ANNOTATION_SPEC.md) is mandatory prior to production underwriting deployment.
