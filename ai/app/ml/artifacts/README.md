# Financial ML Model Artifacts Directory - AgentTrust OS

Place versioned trained financial ML model weight files in this directory:

- `risk_model.json` (XGBoost Credit Risk Booster model weights)
- `fraud_model.txt` (LightGBM Fraud Classification Booster model weights)
- `isolation_forest.joblib` (scikit-learn Isolation Forest estimator artifact)

Configure model paths in environment variables (`RISK_MODEL_PATH`, `FRAUD_MODEL_PATH`, `ANOMALY_MODEL_PATH`).
