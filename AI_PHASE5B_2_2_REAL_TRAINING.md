# Phase 5B.2.2 — Genuine YOLO Document Layout Training Execution Report

**Status**: **COMPLETED & EMPIRICALLY VERIFIED**  
**Date**: August 26, 2026  
**Lead AI/ML Engineer**: Member 3 (AgentTrust OS AI/ML Team)

---

## Executive Summary

Phase 5B.2.2 successfully enabled a real PyTorch / Ultralytics YOLOv8 document-layout training environment on Windows by overcoming the `WINDOWS_MAX_PATH` path length limitation (`[WinError 206]`). Utilizing a short virtual environment path (`C:\atv`), the complete training pipeline was executed with **real gradient backpropagation across 3 PyTorch epochs** on the real 90-page DocLayNet dataset subset.

A genuine **6.25 MB binary PyTorch model checkpoint** (`yolov8_doclayout_v1.pt`) was produced and verified via `torch.load()` and `YOLO()`. Validation metrics were extracted directly from the Ultralytics evaluation run without hardcoded fallbacks or fabricated figures. Real model inference was executed against a held-out test image using the trained checkpoint.

---

## 1. Environment Inspection & MAX_PATH Resolution

- **Root Blocker Identified**: Windows Store Python default path exceeded the 260-character `MAX_PATH` limit when extracting deep PyTorch/Ultralytics C extensions (`[WinError 206]`).
- **Short Path Solution**: Created isolated virtual environment at `C:\atv` (`python -m venv C:\atv`).
- **Environment Verification**:
  - Python Executable: `C:\atv\Scripts\python.exe` (v3.11.9)
  - PyTorch Version: `2.13.0+cpu`
  - Ultralytics Version: `8.4.129`
  - Import Check: `import torch; from ultralytics import YOLO` -> **`ULTRALYTICS_OK`**

---

## 2. Dataset Verification

Pre-training integrity audit confirmed 90 real DocLayNet page images and bounding box annotations $[0..10]$ across standard splits:

| Split | Images | Annotations | Label Bounds Check | Image Decodability |
| :--- | :---: | :---: | :---: | :---: |
| **Train** | 62 | 1,102 | Passed $[0..10]$ | 100% Valid PNG |
| **Val** | 13 | 165 | Passed $[0..10]$ | 100% Valid PNG |
| **Test** | 15 | 119 | Passed $[0..10]$ | 100% Valid PNG |
| **Total** | **90** | **1,386** | **Passed** | **100% Valid** |

---

## 3. Real Training Execution & Log Output

Training was launched via the dedicated training module using CPU execution:
```bash
C:\atv\Scripts\python.exe -m ai.app.ml.training.train_document_layout \
    --dataset data/processed/dataset.yaml \
    --epochs 3 \
    --batch-size 4 \
    --image-size 640 \
    --seed 42 \
    --device cpu \
    --model yolov8n.pt \
    --output-dir artifacts/training/doc_layout/real_yolo_001
```

### PyTorch Epoch Progress & Backpropagation Log

- **Optimizer**: `AdamW(lr=0.002, momentum=0.9, weight_decay=0.0005)`
- **Loss Computation**: Real box loss (`box_loss`), class loss (`cls_loss`), and distribution focal loss (`dfl_loss`) evaluated per batch.
- **Epoch Summary**:
  - **Epoch 1/3**: `box_loss = 2.451`, `cls_loss = 4.120`, `dfl_loss = 1.710`
  - **Epoch 2/3**: `box_loss = 2.312`, `cls_loss = 3.980`, `dfl_loss = 1.602`
  - **Epoch 3/3**: `box_loss = 2.266`, `cls_loss = 3.945`, `dfl_loss = 1.566`
- **Execution Duration**: `0.069 hours` (~4.1 minutes on CPU).

---

## 4. Model Artifact Forensics & Verification

- **Primary Checkpoint Path**: `artifacts/training/doc_layout/real_yolo_001/yolov8_doclayout_v1.pt`
- **Ultralytics Weight Path**: `runs/detect/artifacts/training/doc_layout/real_yolo_001/train_run/weights/best.pt`
- **Exact File Size**: `6,247,786 bytes` (~6.25 MB)
- **SHA-256 Hash**: `09ca9242843a2f1e99fd86d718129d32728813f799adc12a99b83502042771af`
- **PyTorch Loadability (`torch.load`)**: **PASSED** (Loaded valid PyTorch dictionary containing 73 layers state dict).
- **Ultralytics Model Loadability (`YOLO()`)**: **PASSED** (Loaded 3,012,993 parameters across 11 class names).
- **Training Artifact Logging**: `results.csv` logged 3 epoch rows under `runs/detect/artifacts/training/doc_layout/real_yolo_001/train_run/results.csv`.

---

## 5. Genuine Empirical Validation Metrics

Validation metrics were extracted directly from the Ultralytics validation run on the 13 held-out validation images:

### Overall Model Metrics

| Metric | Empirical Value | Provenance / Source |
| :--- | :---: | :--- |
| **mAP@50** | **0.0295** | Direct Ultralytics Validation (`val_results.box.map50`) |
| **mAP@50-95** | **0.0080** | Direct Ultralytics Validation (`val_results.box.map`) |
| **Precision** | **0.0132** | Direct Ultralytics Validation (`val_results.box.mp`) |
| **Recall** | **0.2362** | Direct Ultralytics Validation (`val_results.box.mr`) |
| **Inference Speed** | **18.5 ms** | Measured PyTorch forward pass |

### Per-Class Metric Breakdown

| Class Name | Instances | Precision | Recall | mAP@50 | mAP@50-95 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `FIGURE` | 3 | 0.0299 | 0.667 | 0.1460 | 0.0293 |
| `TABLE` | 8 | 0.0196 | 0.500 | 0.0221 | 0.0111 |
| `TEXT_BLOCK` | 74 | 0.0675 | 0.459 | 0.0856 | 0.0277 |
| `TITLE` | 4 | 0.00216 | 0.500 | 0.0117 | 0.00359 |

---

## 6. Real Model Inference on Held-Out Test Image

Executed forward pass using `YOLO("artifacts/training/doc_layout/real_yolo_001/yolov8_doclayout_v1.pt")` on held-out test image `1a15b0830d7cef153078b9830981320626c2fbcdb7cb344ba477e5d5c25b31aa.png`:
- **Model Loading**: Successfully loaded fused PyTorch model (73 layers, 3,007,793 parameters).
- **Execution Status**: Clean execution without runtime exceptions.
- **Inference Speed**: 18.5 ms per image.

---

## 7. Model Registry Manifest Integration

Manifest `exp_doclayout_9141aa20_manifest.json` registered in `ModelRegistryManager`:
- **Experiment ID**: `exp_doclayout_9141aa20`
- **Model Name**: `YOLOv8-DocLayout-Real`
- **Lifecycle Status**: `EXPERIMENTAL` / `CANDIDATE`
- **Metric Provenance Tag**: `ACTUAL_ULTRALYTICS_METRIC`

---

## 8. Metric Provenance & Correction of Prior Mock Metric Claims

> [!IMPORTANT]
> **Prior Mock Metric Correction**: Previous figures (`mAP50 = 0.412`, `mAP50-95 = 0.284`, `Precision = 0.521`, `Recall = 0.489`) reported during Phase 5B dry-runs were script fallback fixtures caused by the Windows MAX_PATH blocker. They have been officially marked as **`MOCK/FIXTURE (SUPERSEDED)`** in all repository documentation. The genuine empirical baseline on 90 real DocLayNet pages for 3 epochs is **`mAP50 = 0.0295`**.

---

## 9. Comprehensive System Test Suite Verification

- **AI Subsystem Suite (`ai/tests/`)**: **176 PASSED / 3 SKIPPED** (100% of runnable tests passed).
- **Full Platform Suite (`backend/app/tests/ ai/tests/`)**: **196 PASSED / 3 SKIPPED** (100% of runnable tests passed).
- **Skipped Test Note**: 3 PostgreSQL + pgvector tests skipped due to missing local database service, as expected.

---

## Final Verification Checklist

1. [x] Python/pip environment and MAX_PATH bypass verified via short venv `C:\atv`.
2. [x] Genuine Ultralytics (v8.4.129) and PyTorch (v2.13.0+cpu) installed and operational.
3. [x] 90 real DocLayNet images and label bounds $[0..10]$ verified prior to training.
4. [x] Isolation directory `artifacts/training/doc_layout/real_yolo_001/` created.
5. [x] Real 3-epoch CPU training executed with real PyTorch loss minimization and backpropagation.
6. [x] Genuine 6.25 MB binary checkpoint `yolov8_doclayout_v1.pt` produced and verified loadable via `torch.load()` and `YOLO()`.
7. [x] Genuine validation metrics (`mAP50 = 0.0295`) extracted directly from Ultralytics validation run.
8. [x] Real inference executed against held-out test image using the trained checkpoint.
9. [x] Model registered in `ModelRegistryManager` as `EXPERIMENTAL`/`CANDIDATE`.
10. [x] Prior mock metrics documented as superseded in `AI_DOCUMENT_TRAINING_PIPELINE.md`.
11. [x] Full platform test suite verified (196 passed / 3 skipped).
12. [x] Phase 5C NOT started. Frontend and financial backend left completely unmodified.
