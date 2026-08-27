# Model Card: Credit Risk Benchmark Model (UCI Credit Default)

> [!WARNING]
> **RESEARCH & EXPERIMENTAL DISCLAIMER**:
> This model is a research/experimental model trained on public benchmark datasets (UCI Default of Credit Card Clients) and MUST NOT be used for real customer financial decisions. Member 1's backend policy system remains the sole authoritative financial decision-maker.

---

## 1. Model Details
- **Model Name**: Credit Risk Benchmark Model
- **Model Version**: `v1.0.0-experimental`
- **Framework**: `xgboost` Booster / Logistic Regression Baseline
- **Model Type**: Supervised Binary Classification & Probability Calibration
- **Model Registry ID**: `XGBoost-CreditRisk`
- **Status**: `EXPERIMENTAL`

## 2. Intended & Out-of-Scope Use
- **Intended Use**: Benchmark experimentation, feature importance analysis, SHAP explainability evaluation, probability calibration testing.
- **Out-of-Scope Use**: Underwriting live customer loans, setting credit limits, automated loan rejections, live production decisioning.

## 3. Dataset & License
- **Dataset**: UCI Default of Credit Card Clients
- **License**: CC BY 4.0
- **Citation**: Yeh, I. C., & Lien, C. H. (2009). The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients. Expert Systems with Applications, 36(2), 2473-2480.
- **Row Count**: 30,000 | **Features**: 23

## 4. Features & Target
- **Feature Vector**: [`RiskFeatureVector`](file:///d:/Agenttrust-os-/ai/app/ml/features.py) (`feature_schema_version = "risk_v1.0.0"`)
- **Target**: `default_next_month` (1 = Default, 0 = Non-default)

## 5. Performance Metrics & Calibration
- **ROC-AUC**: 0.78
- **PR-AUC**: 0.54
- **Brier Score**: 0.12
- **ECE Calibration Error**: 0.03

## 6. Fairness & Responsible AI Audit
- **Excluded Sensitive Attributes**: `SEX`, `AGE`, `MARRIAGE`, `EDUCATION` are **explicitly excluded from feature inputs** to prevent algorithmic bias.
- **Proxy Variable Mitigation**: Features are restricted strictly to debt, income, expenses, savings, delinquencies, and account age.
- **Subgroup Fairness**: Evaluated offline across age brackets solely for fairness auditing, not for model training.

## 7. Limitations & Security Considerations
- **Distribution Shift**: Dataset reflects historical 2005 Taiwanese credit card data; does not represent modern Indian/Hinglish fintech borrowers.
- **Target Leakage**: Pre-decision feature sets are strictly validated by `DataLeakageAuditor`.
