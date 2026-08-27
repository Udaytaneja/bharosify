# AI ML Experimentation & Reproducibility Guide - AgentTrust OS

**Author**: Member 3 (AI/ML/LLM/Agent Intelligence Subsystem Lead)  
**Date**: August 25, 2026  
**Scope**: Step-by-Step Experimentation & Reproducibility Walkthrough

---

## How to Reproduce an Experiment

### 1. Credit Risk Benchmark Training Experiment
To run the Credit Risk XGBoost benchmark training experiment against the Logistic Regression baseline:
```bash
python -m ai.app.ml.training.train_risk --dataset uci_credit_default --seed 42
```

### 2. Fraud & Synthetic AML Experiment
To run the LightGBM synthetic AML training experiment (`DATA_TYPE = SYNTHETIC`):
```bash
python -m ai.app.ml.training.train_fraud --dataset ibm_aml_synthetic --seed 42
```

### 3. Transaction Anomaly Experiment
To run the Isolation Forest transaction anomaly training experiment:
```bash
python -m ai.app.ml.training.train_anomaly --seed 42
```

---

## Experiment Manifest Verification

Every training experiment generates an immutable experiment manifest stored in `ExperimentManifestManager`:
- `model_id`: Unique experiment ID (e.g. `exp_risk_uci_credit_default_seed42`)
- `random_seed`: Deterministic random seed
- `metrics`: ROC-AUC, PR-AUC, Precision, Recall, F1, Brier Score, ECE Calibration Error
- `checksum`: MD5 artifact checksum
- `status`: `EXPERIMENTAL`
