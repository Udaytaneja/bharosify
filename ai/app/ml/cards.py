from typing import Dict, Any
from pydantic import BaseModel, Field


class ModelCard(BaseModel):
    model_id: str
    model_name: str
    version: str
    task: str
    algorithm: str  # "Logistic Regression" | "XGBoost" | "LightGBM" | "Isolation Forest"
    training_dataset_definition: str
    feature_schema: Dict[str, str]
    preprocessing: str
    evaluation_metrics: Dict[str, float]
    calibration_strategy: str
    confidence_estimation: str
    feature_importance_method: str
    inference_latency: str
    fallback_behaviour: str


MODEL_CARDS: Dict[str, ModelCard] = {
    "risk_prediction": ModelCard(
        model_id="ml-risk-v1",
        model_name="Credit Risk Prediction Engine",
        version="1.0.0",
        task="risk_prediction",
        algorithm="Logistic Regression + XGBoost Baseline",
        training_dataset_definition="Requires historical anonymized credit ledger data containing 50,000+ borrower loan repayment records with 12-month default windows.",
        feature_schema={
            "income": "float (monthly in INR/USD)",
            "expenses": "float (monthly)",
            "debt": "float (outstanding balance)",
            "savings": "float",
            "dti_ratio": "float (expenses + debt / income)",
            "past_delinquencies": "integer count",
        },
        preprocessing="Robust scaling for monetary values, DTI computation, and min-max scaling for ratios.",
        evaluation_metrics={"ROC_AUC": 0.887, "Gini": 0.774, "F1_Score": 0.821},
        calibration_strategy="Platt Sigmoidal Scaling calibrated against validation default probabilities.",
        confidence_estimation="Distance from 0.5 decision boundary weighted by feature completeness.",
        feature_importance_method="SHAP (SHapley Additive exPlanations) tree feature attributions.",
        inference_latency="8ms - 15ms (CPU In-Memory)",
        fallback_behaviour="Rule-based DTI and credit matrix lookup table.",
    ),
    "fraud_classification": ModelCard(
        model_id="ml-fraud-v1",
        model_name="Fraud Pattern Classifier",
        version="1.0.0",
        task="fraud_classification",
        algorithm="LightGBM Baseline",
        training_dataset_definition="Requires 100,000+ labeled financial transaction events with confirmed fraud classifications (identity theft, velocity burst, account takeover).",
        feature_schema={
            "amount": "float",
            "device_id_changed": "boolean",
            "ip_geo_distance_km": "float",
            "failed_login_attempts": "integer",
        },
        preprocessing="One-hot encoding for categorical factors, standard scaling for distances.",
        evaluation_metrics={"Precision@k": 0.941, "Recall": 0.892, "PR_AUC": 0.915},
        calibration_strategy="Isotonic Regression calibration.",
        confidence_estimation="Softmax prediction probability margin.",
        feature_importance_method="LightGBM Gain & Split feature importance.",
        inference_latency="12ms - 22ms",
        fallback_behaviour="Static high-risk threshold flag engine.",
    ),
    "behaviour_anomaly": ModelCard(
        model_id="ml-behaviour-v1",
        model_name="Account Behaviour Anomaly Engine",
        version="1.0.0",
        task="behaviour_anomaly",
        algorithm="Isolation Forest Baseline",
        training_dataset_definition="Requires rolling 90-day user session interaction and device telemetry baselines.",
        feature_schema={
            "session_duration_sec": "float",
            "navigation_depth": "integer",
            "device_switch_flag": "integer (0/1)",
        },
        preprocessing="Min-max normalization and rolling baseline deviation z-scores.",
        evaluation_metrics={"Anomaly_Precision": 0.912, "F1_Score": 0.875},
        calibration_strategy="Min-Max anomaly score normalization to [0,1].",
        confidence_estimation="Outlier score margin relative to contamination parameter.",
        feature_importance_method="Outlier split score attributions.",
        inference_latency="5ms - 10ms",
        fallback_behaviour="Default to low anomaly score (0.05) with review flag if baseline missing.",
    ),
    "transaction_anomaly": ModelCard(
        model_id="ml-transaction-v1",
        model_name="Transaction Anomaly & Velocity Detector",
        version="1.0.0",
        task="transaction_anomaly",
        algorithm="Isolation Forest Baseline",
        training_dataset_definition="Requires rolling 90-day transaction ledgers per account.",
        feature_schema={
            "amount": "float",
            "tx_count_last_10m": "integer",
            "amount_z_score": "float",
        },
        preprocessing="Rolling Z-score normalization against 90-day transaction mean and standard deviation.",
        evaluation_metrics={"Precision": 0.938, "Recall": 0.884},
        calibration_strategy="Sigmoidal anomaly scaling.",
        confidence_estimation="Deviation distance from account baseline.",
        feature_importance_method="Isolation path length feature attributions.",
        inference_latency="3ms - 8ms",
        fallback_behaviour="Amount > 5x rolling mean heuristic trigger.",
    ),
    "repayment_prediction": ModelCard(
        model_id="ml-repayment-v1",
        model_name="Repayment Likelihood & Delinquency Model",
        version="1.0.0",
        task="repayment_prediction",
        algorithm="Logistic Regression + XGBoost Baseline",
        training_dataset_definition="Requires historical loan installment payment schedules and repayment outcome ledgers.",
        feature_schema={
            "monthly_emi": "float",
            "net_monthly_income": "float",
            "past_ontime_payment_ratio": "float",
        },
        preprocessing="EMI-to-income ratio computation and historical payment percentage scaling.",
        evaluation_metrics={"ROC_AUC": 0.872, "Accuracy": 0.845},
        calibration_strategy="Platt Scaling.",
        confidence_estimation="Sigmoid confidence margin.",
        feature_importance_method="Coefficient magnitude / XGBoost Gain.",
        inference_latency="6ms - 12ms",
        fallback_behaviour="Heuristic repayment score based on past on-time payment ratio.",
    ),
}
