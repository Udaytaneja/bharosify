import pytest
from pydantic import ValidationError

from ai.app.core.config import ai_settings
from ai.app.models.model_lifecycle import model_registry_manager
from ai.app.ml.features import (
    BehaviourAnomalyFeatureVector,
    FeaturePreprocessor,
    FraudFeatureVector,
    RiskFeatureVector,
    TransactionAnomalyFeatureVector,
    feature_preprocessor,
)
from ai.app.ml.fraud_model import fraud_classification_model
from ai.app.ml.interfaces import FraudClassificationSignal, RiskPredictionSignal, TransactionAnomalySignal
from ai.app.ml.risk_model import risk_prediction_model
from ai.app.ml.transaction_anomaly import transaction_anomaly_model
from ai.app.ml.training.leakage_audit import data_leakage_auditor


@pytest.mark.asyncio
async def test_1_risk_feature_vector_validation():
    feats = feature_preprocessor.extract_risk_features(
        {
            "income": 120000.0,
            "expenses": 30000.0,
            "debt": 15000.0,
            "savings": 50000.0,
            "requested_amount": 25000.0,
            "account_age_months": 36.0,
            "past_delinquencies": 0.0,
        }
    )
    assert isinstance(feats, RiskFeatureVector)
    assert feats.feature_schema_version == "risk_v1.0.0"
    assert feats.dti_ratio == 0.375
    assert len(feats.to_numpy()) == 10

    # Negative income validation error
    with pytest.raises(ValidationError):
        RiskFeatureVector(
            income=-500,
            expenses=100,
            debt=0,
            savings=0,
            requested_amount=1000,
            dti_ratio=0.1,
            savings_to_debt_ratio=1.0,
            loan_to_income_ratio=0.5,
            account_age_months=12,
            past_delinquencies=0,
        )


@pytest.mark.asyncio
async def test_2_xgboost_risk_model_predict_and_score_mapping():
    applicant_data = {
        "income": 150000.0,
        "expenses": 25000.0,
        "debt": 5000.0,
        "savings": 80000.0,
        "requested_amount": 20000.0,
        "account_age_months": 48.0,
        "past_delinquencies": 0.0,
    }

    signal: RiskPredictionSignal = await risk_prediction_model.predict_risk(applicant_data)
    assert isinstance(signal, RiskPredictionSignal)
    assert 300 <= signal.risk_score <= 850
    assert signal.risk_score >= 700
    assert signal.risk_level in ["low", "medium"]
    assert signal.suggested_decision in ["approve", "review"]
    assert "calibrated-fallback" in signal.model_version
    assert len(signal.attributions) > 0


@pytest.mark.asyncio
async def test_3_lightgbm_fraud_model_signal_generation():
    fraud_event = {
        "amount": 250000.0,
        "failed_login_count": 6,
        "tx_velocity_10m": 8,
        "device_switch_flag": True,
        "unusual_ip_flag": True,
    }

    signal: FraudClassificationSignal = await fraud_classification_model.classify_fraud(fraud_event)
    assert isinstance(signal, FraudClassificationSignal)
    assert signal.fraud_score >= 0.75
    assert signal.fraud_type == "account_takeover"
    assert signal.severity in ["high", "critical"]
    assert len(signal.attributions) >= 2


@pytest.mark.asyncio
async def test_4_isolation_forest_transaction_anomaly_detection():
    tx = {"amount": 15000.0, "tx_count_last_10m": 12.0}
    baseline = {"average_transaction_amount": 100.0, "std_transaction_amount": 25.0}

    signal: TransactionAnomalySignal = await transaction_anomaly_model.detect_transaction_anomaly(tx, baseline)
    assert isinstance(signal, TransactionAnomalySignal)
    assert signal.is_anomalous is True
    assert signal.anomaly_score >= 0.70
    assert signal.amount_deviation_sigma > 3.0
    assert len(signal.anomalous_features) >= 1


def test_5_data_leakage_audit():
    valid_features = ["income", "dti_ratio", "savings_to_debt_ratio", "past_delinquencies"]
    passed, violations = data_leakage_auditor.audit_feature_set(valid_features)
    assert passed is True
    assert len(violations) == 0

    leaky_features = ["income", "repayment_status", "default_flag", "chargeoff_date"]
    passed, violations = data_leakage_auditor.audit_feature_set(leaky_features)
    assert passed is False
    assert len(violations) == 3


def test_6_model_registry_phase2b_tracking():
    xgb_meta = model_registry_manager.get_metadata("XGBoost-CreditRisk")
    assert xgb_meta is not None
    assert xgb_meta.provider == "xgboost"

    lgb_meta = model_registry_manager.get_metadata("LightGBM-FraudClassifier")
    assert lgb_meta is not None
    assert lgb_meta.provider == "lightgbm"

    iforest_meta = model_registry_manager.get_metadata("IsolationForest-AnomalyDetector")
    assert iforest_meta is not None
    assert iforest_meta.provider == "scikit-learn"
