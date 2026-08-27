import pytest
from ai.app.ml import (
    risk_prediction_model,
    fraud_classification_model,
    behaviour_anomaly_model,
    transaction_anomaly_model,
    repayment_prediction_model,
    MODEL_CARDS,
    backend_ml_integration,
    RiskPredictionSignal,
    FraudClassificationSignal,
    BehaviourAnomalySignal,
    TransactionAnomalySignal,
    RepaymentPredictionSignal,
)


@pytest.mark.asyncio
async def test_risk_prediction_model():
    applicant_data = {
        "income": 100000.0,
        "expenses": 25000.0,
        "debt": 10000.0,
        "savings": 30000.0,
        "requested_amount": 20000.0,
        "account_age_months": 24,
        "past_delinquencies": 0,
    }

    signal = await risk_prediction_model.predict_risk(applicant_data)
    assert isinstance(signal, RiskPredictionSignal)
    assert 300 <= signal.risk_score <= 850
    assert 0.0 <= signal.probability_of_default <= 1.0
    assert signal.risk_level in ["low", "medium", "high", "critical"]
    assert len(signal.attributions) >= 1
    assert signal.suggested_decision in ["approve", "review", "reject", "escalate"]


@pytest.mark.asyncio
async def test_fraud_classification_model():
    clean_event = {"failed_login_attempts": 0, "device_id_changed": False}
    clean_signal = await fraud_classification_model.classify_fraud(clean_event)
    assert clean_signal.fraud_score < 0.20
    assert clean_signal.fraud_type == "normal"

    suspicious_event = {"failed_login_attempts": 6, "device_id_changed": True}
    suspicious_signal = await fraud_classification_model.classify_fraud(suspicious_event)
    assert isinstance(suspicious_signal, FraudClassificationSignal)
    assert suspicious_signal.fraud_score > 0.70
    assert suspicious_signal.severity == "high"


@pytest.mark.asyncio
async def test_behaviour_anomaly_model():
    session_data = {"session_duration_sec": 3.0, "navigation_depth": 15, "device_switch_flag": True}
    baseline = {"avg_session_duration": 150.0}

    signal = await behaviour_anomaly_model.detect_behaviour_anomaly(session_data, baseline)
    assert isinstance(signal, BehaviourAnomalySignal)
    assert signal.is_anomalous is True
    assert signal.anomaly_score > 0.50
    assert len(signal.anomalous_features) >= 1


@pytest.mark.asyncio
async def test_transaction_anomaly_model():
    normal_tx = {"amount": 60.0, "tx_count_last_10m": 1}
    baseline = {"average_transaction_amount": 50.0, "std_transaction_amount": 10.0}
    normal_signal = await transaction_anomaly_model.detect_transaction_anomaly(normal_tx, baseline)
    assert normal_signal.is_anomalous is False

    anomalous_tx = {"amount": 5000.0, "tx_count_last_10m": 10}
    anomalous_signal = await transaction_anomaly_model.detect_transaction_anomaly(anomalous_tx, baseline)
    assert isinstance(anomalous_signal, TransactionAnomalySignal)
    assert anomalous_signal.is_anomalous is True
    assert anomalous_signal.severity == "high"


@pytest.mark.asyncio
async def test_repayment_prediction_model():
    loan_features = {"income": 80000.0, "monthly_emi": 15000.0}
    payment_history = {"past_ontime_payment_ratio": 0.98}

    signal = await repayment_prediction_model.predict_repayment(loan_features, payment_history)
    assert isinstance(signal, RepaymentPredictionSignal)
    assert signal.repayment_probability >= 0.85
    assert signal.delinquency_tier == "on_time"


def test_model_cards_retrieval():
    assert "risk_prediction" in MODEL_CARDS
    assert "fraud_classification" in MODEL_CARDS
    assert "behaviour_anomaly" in MODEL_CARDS
    assert "transaction_anomaly" in MODEL_CARDS
    assert "repayment_prediction" in MODEL_CARDS

    card = MODEL_CARDS["risk_prediction"]
    assert card.algorithm == "Logistic Regression + XGBoost Baseline"
    assert "ROC_AUC" in card.evaluation_metrics
    assert len(card.training_dataset_definition) > 0


@pytest.mark.asyncio
async def test_backend_integration_mapping():
    applicant_data = {"income": 100000.0, "debt": 10000.0, "expenses": 20000.0}
    risk_sig = await risk_prediction_model.predict_risk(applicant_data)

    risk_orm = backend_ml_integration.to_risk_assessment_model(customer_id=42, signal=risk_sig)
    assert risk_orm.customer_id == 42
    assert risk_orm.score == risk_sig.risk_score
    assert risk_orm.confidence == risk_sig.confidence

    fraud_sig = await fraud_classification_model.classify_fraud({"failed_login_attempts": 5, "device_id_changed": True})
    fraud_orm = backend_ml_integration.to_fraud_signal_model(customer_id=42, transaction_id=101, signal=fraud_sig)
    assert fraud_orm.customer_id == 42
    assert fraud_orm.transaction_id == 101
    assert fraud_orm.status == "open"

    trust_factors = backend_ml_integration.to_trust_factors(trust_profile_id=1, risk_signal=risk_sig)
    assert len(trust_factors) >= 1
    assert trust_factors[0].trust_profile_id == 1
