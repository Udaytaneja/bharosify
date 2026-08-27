# Model Card: Transaction Anomaly Benchmark Model (Isolation Forest)

> [!WARNING]
> **RESEARCH & EXPERIMENTAL DISCLAIMER**:
> This model is a research/experimental model for anomaly detection and MUST NOT be used for real customer financial decisioning.

---

## 1. Model Details
- **Model Name**: Isolation Forest Transaction Anomaly Benchmark Model
- **Model Version**: `v1.0.0-experimental`
- **Framework**: `scikit-learn` IsolationForest Estimator
- **Model Registry ID**: `IsolationForest-AnomalyDetector`
- **Status**: `EXPERIMENTAL`

## 2. Intended Use & Features
- **Features**: Amount Z-Score $\frac{X - \mu}{\sigma}$, velocity ratio, device switch flag.
- **Target**: Anomaly score (0.0 to 1.0) and binary `is_anomalous` flag.
