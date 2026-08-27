# Financial ML Empirical Verification Report - AgentTrust OS

**Author**: Member 3 (AI/ML/LLM/Agent Intelligence Subsystem Lead)  
**Date**: August 25, 2026  
**Scope**: Empirical Verification Audit of ML Benchmark Metrics & Dataset Availability

---

## Executive Summary

| Model | Dataset Target | Local Dataset Availability | Empirical Verification Status |
| :--- | :--- | :--- | :--- |
| **XGBoost Credit Risk Model** | UCI Default of Credit Card Clients | **NOT PRESENT** (`data/raw/uci_credit_default.csv` missing) | **NOT VERIFIED (`DATASET NOT PRESENT — METRICS NOT EMPIRICALLY VERIFIED`)** |
| **LightGBM Fraud Model** | IBM AML-Data (Synthetic) | **NOT PRESENT** (`data/raw/ibm_aml_synthetic.csv` missing) | **NOT VERIFIED (`DATASET NOT PRESENT — METRICS NOT EMPIRICALLY VERIFIED`)** |
| **Isolation Forest Anomaly Model** | IBM AMLSim Graph / Transaction | **NOT PRESENT** (`data/raw/ibm_aml_synthetic.csv` missing) | **NOT VERIFIED (`DATASET NOT PRESENT — METRICS NOT EMPIRICALLY VERIFIED`)** |

---

## 1. Credit Risk Model Empirical Verification

- **Reported Narrative Figures**: `XGBoost ROC-AUC = 0.78`, `Logistic Regression ROC-AUC = 0.68`.
- **Dataset Availability Check**: File `data/raw/uci_credit_default.csv` is **NOT PRESENT** on local disk. Per explicit safety guidelines, zero external files were downloaded automatically.
- **Empirical Execution Audit**: Executed `python -m ai.app.ml.training.train_risk` using deterministic sample mock fixture (200 rows).
  - Executed Metrics: `ROC-AUC = 0.9785`, `PR-AUC = 0.9403`, `Precision = 0.9118`, `Recall = 0.9688`, `F1 = 0.9394`, `Brier Score = 0.0801`, `ECE Calibration Error = 0.1368`.
  - Confusion Matrix: `TP: 31, FP: 3, TN: 5, FN: 1`.
- **Match Determination**: The narrative metrics (0.78 and 0.68) **DO NOT MATCH** the mock execution results, confirming that 0.78/0.68 were narrative/illustrative figures rather than empirically derived from the full 30,000-row UCI Credit Default CSV file.
- **Target Leakage Check**: `DataLeakageAuditor` verified zero target leakage in feature schemas (`passed_audit = True`).
- **Final Status**: **`NOT VERIFIED (DATASET NOT PRESENT — METRICS NOT EMPIRICALLY VERIFIED)`**

---

## 2. Fraud Classification Model Empirical Verification

- **Dataset Availability Check**: File `data/raw/ibm_aml_synthetic.csv` is **NOT PRESENT** on local disk.
- **Empirical Execution Audit**: Executed `python -m ai.app.ml.training.train_fraud` using deterministic sample mock fixture.
  - Executed Metrics: `ROC-AUC = 0.9850`, `PR-AUC = 0.9520`, `Precision = 0.9200`, `Recall = 0.9500`, `F1 = 0.9348`.
- **Final Status**: **`NOT VERIFIED (DATASET NOT PRESENT — METRICS NOT EMPIRICALLY VERIFIED)`**

---

## 3. Transaction Anomaly Model Empirical Verification

- **Dataset Availability Check**: File `data/raw/ibm_aml_synthetic.csv` is **NOT PRESENT** on local disk.
- **Empirical Execution Audit**: Executed `python -m ai.app.ml.training.train_anomaly` using sample fixture.
  - Executed Metrics: `Precision = 1.0`, `Recall = 1.0`, `F1 = 1.0`, `FPR = 0.0`.
- **Final Status**: **`NOT VERIFIED (DATASET NOT PRESENT — METRICS NOT EMPIRICALLY VERIFIED)`**

---

## Verification Test Run Summary

```bash
python -m pytest ai/tests/
```
Output: **`94 passed in 2.58s`**

```bash
python -m pytest backend/app/tests/ ai/tests/
```
Output: **`114 passed in 12.31s (100% pass rate)`**
