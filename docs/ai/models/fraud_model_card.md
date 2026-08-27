# Model Card: Synthetic AML & Fraud Pattern Benchmark Model (IBM AML-Data)

> [!WARNING]
> **RESEARCH & EXPERIMENTAL DISCLAIMER**:
> This model is a research/experimental model trained on synthetic IBM AML transaction datasets (`DATA_TYPE = SYNTHETIC`) and MUST NOT be used for real customer transaction blocking. Member 1's backend policy system remains the sole authoritative transaction decision-maker.

---

## 1. Model Details
- **Model Name**: LightGBM Synthetic AML Benchmark Model
- **Model Version**: `v1.0.0-synthetic-experimental`
- **Framework**: `lightgbm` Booster / Logistic Regression Baseline
- **Model Type**: Supervised Binary Fraud Classification & Signal Generation
- **Model Registry ID**: `LightGBM-FraudClassifier`
- **Status**: `EXPERIMENTAL`

## 2. Intended & Out-of-Scope Use
- **Intended Use**: Velocity spike detection testing, failed login escalation, synthetic AML pattern research.
- **Out-of-Scope Use**: Real customer transaction blocking, automated SAR filing.

## 3. Dataset & License
- **Dataset**: IBM Anti-Money Laundering Synthetic Transaction Data
- **License**: CDLA-Sharing-1.0
- **Data Type**: `SYNTHETIC`
- **Citation**: Altman, E. (2023). Synthetic Financial Transactions Dataset for AML. IBM Research.

## 4. Features & Target
- **Feature Vector**: [`FraudFeatureVector`](file:///d:/Agenttrust-os-/ai/app/ml/features.py) (`feature_schema_version = "fraud_v1.0.0"`)
- **Target**: `is_laundering` (1 = Laundering / Suspicious, 0 = Legitimate)

## 5. Non-Authoritative Boundary
- Emits fraud risk signals (`FraudClassificationSignal`) ONLY.
- AI layer never directly blocks a financial transaction.
