# Phase 5B.7 - Indian-Domain Document Layout Fine-Tuning

**Date:** 2026-08-26  
**Status:** **BLOCKED - TRAINING NOT EXECUTED**  
**Model status:** **EXPERIMENTAL**

## Decision

Phase 5B.7 was stopped before training. The only available Indian-domain
dataset is explicitly identified by its manifest as synthetic, while this
phase requires a verified real dataset. The acquisition report also marks the
dataset `READY FOR TRAINING: NO`. Training against it would violate the phase
rules.

The active Python environment also does not provide the `ultralytics` package.
Therefore the requested `YOLO()` checkpoint verification, training,
held-out-test evaluation, and inference could not execute. No substitute
metrics, fallback metrics, mock checkpoint, or Phase 5C work was performed.

## Preflight Evidence

### Dataset manifest and mapping

- Manifest: [data/processed/indian_fin_docs/manifest.json](data/processed/indian_fin_docs/manifest.json)
- Dataset ID: `ds_indian_synthetic_bank_statements_5b6`
- Manifest `real_or_synthetic`: `synthetic`
- Dataset YAML: [data/processed/indian_fin_docs/indian_fin_docs.yaml](data/processed/indian_fin_docs/indian_fin_docs.yaml)
- Documents: 375
- Pages/images: 1,500
- YOLO label files: 1,500
- Annotations: 19,500
- Classes: 13

The verified class mapping is the YAML mapping below:

| ID | Class |
|---:|---|
| 0 | `DOCUMENT_HEADER` |
| 1 | `DOCUMENT_TITLE` |
| 2 | `BANK_NAME` |
| 3 | `EMPLOYER_NAME` |
| 4 | `CUSTOMER_NAME` |
| 5 | `ACCOUNT_NUMBER` |
| 6 | `IFSC_CODE` |
| 7 | `DATE_RANGE` |
| 8 | `TRANSACTION_TABLE` |
| 9 | `TABLE_HEADER` |
| 10 | `TOTAL_AMOUNT` |
| 11 | `SIGNATURE` |
| 12 | `STAMP` |

### Split isolation

| Split | Documents | Pages | Template families |
|---|---:|---:|---|
| Train | 262 | 1,050 | `bank-statement-family-00` through `04` |
| Validation | 56 | 225 | `bank-statement-family-05` through `09` |
| Test | 57 | 225 | `bank-statement-family-10` through `14` |

The manifest records `split_document_overlap: false`, and the template-family
sets are disjoint. The manifest records 1,500 instances of each of the 13
classes, for 19,500 annotations total.

### Requested source checkpoint

The requested source checkpoint exists at:

`runs/detect/artifacts/training/doc_layout/real_yolo_002/train_run/weights/best.pt`

Its preflight hash is:

`SHA-256: f1bc0e4d6e4b78f40681d93ce8bb4cf5cd34924bf1efb2ceddbc209d1da40250`

File size is 6,248,042 bytes. No copy was made and no artifact was modified.

## Training Configuration

No training configuration was generated because the run was stopped during
preflight. The intended controlled-run values were seed `42`, image size
`640`, and `5-10` epochs, with batch size selected after hardware/runtime
verification. No `best.pt`, `last.pt`, `results.csv`, or training metrics were
created by Phase 5B.7.

## Evaluation and Inference

Not run. Consequently, there are no truthful Phase 5B.7 values for:

- Precision
- Recall
- mAP@50
- mAP@50-95
- Per-class metrics
- Inference latency

`torch.load()` and `YOLO()` verification of the source checkpoint could not be
completed because importing `ultralytics` failed with:

`ModuleNotFoundError: No module named 'ultralytics'`

This report intentionally does not reuse earlier-phase metrics; those metrics
were produced on a different dataset and are not Phase 5B.7 results.

## Authenticity Chain

| Required link | Result |
|---|---|
| Dataset | **Verified locally, but synthetic and therefore disallowed for this phase** |
| Real training | **Not executed** |
| Real checkpoint | Existing prior checkpoint verified by hash only; no Phase 5B.7 checkpoint |
| Real validation | **Not executed** |
| Real inference | **Not executed** |

The authenticity chain `dataset -> real training -> real checkpoint -> real
validation -> real inference` is therefore **not established**. This is a
blocked phase, not a successful fine-tuning result.

## Required Test Commands

The requested commands were started:

```text
python -m pytest ai/tests/
python -m pytest backend/app/tests/ ai/tests/
```

Their final completion output was not available when this report was written.
These tests do not unblock the dataset or Ultralytics requirements.

## Unblock Conditions

1. Provide a dataset whose provenance and manifest identify it as real Indian-
   domain data, with verified annotations and split isolation.
2. Install and verify a compatible PyTorch/Ultralytics runtime in the active
   interpreter.
3. Restart Phase 5B.7 from the preflight checks, using only
   `real_yolo_002/best.pt` and recording all requested artifacts and measured
   outputs.

Phase 5C was not started.