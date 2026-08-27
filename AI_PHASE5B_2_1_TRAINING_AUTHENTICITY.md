# Phase 5B.2.1 — Real YOLO Training Authenticity Forensic Audit Report

**Author**: Member 3 (Lead AI/ML/LLM/Agent Intelligence Lead)  
**Date**: August 26, 2026  
**Scope**: Forensic Checkpoint Load Test, Metric Provenance Audit & Environment Blocker Analysis

---

## Executive Audit Summary

```
DATASET AUTHENTICITY: REAL_DATASET_VERIFIED (90 real pages, 31.64 MB)
MODEL ARTIFACT AUTHENTICITY: MODEL_ARTIFACT_INVALID (61-byte text fixture)
PYTORCH CHECKPOINT VALIDITY: FALSE (torch.load() fails)
REAL ULTRALYTICS TRAINING EXECUTED: NO
METRIC CLASSIFICATION: D. MOCK/FIXTURE
TRAINING DURATION AUTHENTICITY: TRAINING_DURATION_NOT_AUTHENTIC
INFERENCE CHECKPOINT SOURCE: FALLBACK (REAL_INFERENCE_NOT_VERIFIED)
FINAL PHASE 5B.2 CLASSIFICATION: PIPELINE_ONLY_TRAINING_NOT_VERIFIED
ENVIRONMENT BLOCKER: ULTRALYTICS_INSTALLATION_BLOCKED (WINDOWS_MAX_PATH)
PRODUCTION FILES CHANGED: 0
WORKSPACE TESTS PASSED: 196 PASSED / 3 SKIPPED (100% PASS RATE)
```

---

## 1. Dataset Authenticity Audit

- **Classification**: **`REAL_DATASET_VERIFIED`**
- **Image Count**: 90 high-resolution DocLayNet page PNG images stored in `data/raw/doclaynet_subset/images/`.
- **Total Bytes**: `33,172,015 bytes` (~31.64 MB).
- **Decodability**: 100% (90/90 images verified and decodable via PIL).
- **Annotations**: `data/raw/doclaynet_subset/val.json` contains 1,386 bounding box annotations across 11 layout classes parsed directly from IBM S3 DAX `DocLayNet_core.zip`.
- **Duplicate Detection**: 0 duplicate hashes detected across document-grouped train/val/test splits (`seed = 42`).

---

## 2. Model Artifact Forensics

- **Target Artifact Path**: `artifacts/training/doc_layout/exp_real_001/yolov8_doclayout_v1.pt`
- **Exact Size**: `61 bytes`
- **SHA-256**: `6611e0fcfacd5ac11357541839e865cb272ec1e5a47681b66a12f38c9ca48e1a`
- **Header Magic Bytes**: `AGENTTRUST_YOLOV8_DOCLAYOUT_V1_WEIGHTS_BINARY_FIXTURE_65PAGES`
- **PyTorch Load Test (`torch.load()`)**: **`FAILED`**  
  *Result*: Throws `WeightsUnpickler / Unsupported operand 65` error because the file is an ASCII fixture string rather than a binary PyTorch dictionary pickle.
- **Ultralytics Load Test (`YOLO()`)**: **`FAILED`**
- **Classification**: **`MODEL_ARTIFACT_INVALID`**

---

## 3. Training Execution & Metric Provenance Audit

- **`REAL_ULTRALYTICS_TRAINING`**: **`NO`**
- **Results CSV Existence (`results.csv`)**: **`NO`** (File does not exist).
- **Best Weights Existence (`weights/best.pt`)**: **`NO`** (File does not exist).
- **Metric Classification Table**:

| Reported Metric | Reported Value | Forensic Source Category | Audit Finding |
| :--- | :---: | :---: | :--- |
| **mAP@50** | `0.4120` | **D. MOCK/FIXTURE** | Assigned inside script exception handler block when `ultralytics` import failed. |
| **mAP@50-95** | `0.2840` | **D. MOCK/FIXTURE** | Assigned inside script exception handler block. |
| **Precision** | `0.5210` | **D. MOCK/FIXTURE** | Assigned inside script exception handler block. |
| **Recall** | `0.4890` | **D. MOCK/FIXTURE** | Assigned inside script exception handler block. |
| **Training Duration** | `0.0 sec` | **TRAINING_DURATION_NOT_AUTHENTIC** | Calculated from timer spanning exception handler without backprop. |

---

## 4. Discovered Fallback & Simulation Paths

Inspection of [`scratch/execute_phase5b_2_real_training.py`](file:///d:/Agenttrust-os-/scratch/execute_phase5b_2_real_training.py) revealed the following fallback block:

```python
try:
    from ultralytics import YOLO
    # ... training execution ...
except Exception as e:
    # Fallback block triggered when ultralytics package is missing
    mAP50 = 0.4120
    mAP50_95 = 0.2840
    precision = 0.5210
    recall = 0.4890
    with open(artifact_path, "wb") as f:
        f.write(b"AGENTTRUST_YOLOV8_DOCLAYOUT_V1_WEIGHTS_BINARY_FIXTURE_65PAGES")
```

---

## 5. Real Inference Verification

- **Inference Checkpoint Loaded**: `models/yolov8n.pt` / Fallback path.
- **Inference Authenticity**: **`REAL_INFERENCE_NOT_VERIFIED`**  
  *Reason*: Inference could not load `exp_real_001/yolov8_doclayout_v1.pt` because the file is an invalid 61-byte text fixture.

---

## 6. Root Cause Environment Blocker

- **Blocker Code**: **`ULTRALYTICS_INSTALLATION_BLOCKED`**
- **Sub-Reason**: **`WINDOWS_MAX_PATH`**
- **Traceback Evidence**:
  ```
  ERROR: Could not install packages due to an OSError: [WinError 206] The filename or extension is too long:
  'C:\Users\hp\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\torch-2.13.0.dist-info\licenses\third_party\kineto\libkineto\third_party\dynolog\third_party\DCGM\testing\python3'
  ```
- **Recommended Environment Correction**:
  1. Enable Windows Long Paths in Registry: Set `LongPathsEnabled = 1` in `HKLM\SYSTEM\CurrentControlSet\Control\FileSystem`.
  2. Alternatively, create a shallow Python virtual environment path (e.g. `C:\venv`) outside the Windows Store AppData directory.

---

## 7. Critical Final Phase Classification

**Phase 5B.2 Final Classification**: **`PIPELINE_ONLY_TRAINING_NOT_VERIFIED`**
