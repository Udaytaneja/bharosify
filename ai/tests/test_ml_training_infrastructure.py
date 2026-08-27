import pytest
from ai.app.ml.datasets import DatasetLoader, DatasetMetadata, DatasetValidationError, dataset_loader, dataset_registry_manager
from ai.app.ml.evaluation.metrics import model_evaluator
from ai.app.ml.registry import ModelManifest, experiment_manifest_manager
from ai.app.ml.training.train_anomaly import run_transaction_anomaly_training_experiment
from ai.app.ml.training.train_fraud import run_fraud_aml_training_experiment
from ai.app.ml.training.train_risk import run_credit_risk_training_experiment


def test_1_dataset_registry_registrations():
    ds_uci = dataset_registry_manager.get_dataset("uci_credit_default")
    assert ds_uci is not None
    assert ds_uci.license == "CC BY 4.0"
    assert ds_uci.status == "APPROVED_FOR_RESEARCH"
    assert "SEX" in ds_uci.sensitive_attributes

    ds_ibm = dataset_registry_manager.get_dataset("ibm_aml_synthetic")
    assert ds_ibm is not None
    assert ds_ibm.license == "CDLA-Sharing-1.0"
    assert ds_ibm.is_synthetic is True


def test_2_dataset_loader_schema_validation():
    mock_rows = [
        {"income": 50000, "debt": 10000, "default_next_month": 0},
        {"income": 120000, "debt": 5000, "default_next_month": 0},
    ]
    rows, val_meta = dataset_loader.load_dataset("uci_credit_default", sample_mock_rows=mock_rows)
    assert len(rows) == 2
    assert val_meta["validation_passed"] is True

    # Invalid dataset without target column raises error
    invalid_rows = [{"income": 50000, "debt": 10000}]
    with pytest.raises(DatasetValidationError):
        dataset_loader.load_dataset("uci_credit_default", sample_mock_rows=invalid_rows)


def test_3_model_evaluation_metrics_and_calibration():
    y_true = [0, 0, 0, 0, 1, 1, 1, 1]
    y_prob = [0.05, 0.08, 0.04, 0.02, 0.95, 0.92, 0.98, 0.94]

    base_prob = [0.2, 0.3, 0.35, 0.40, 0.60, 0.65, 0.55, 0.70]

    res = model_evaluator.evaluate_binary_classifier(y_true, y_prob, baseline_prob=base_prob)
    metrics = res["metrics"]

    assert metrics["accuracy"] == 1.0
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 1.0
    assert metrics["f1"] == 1.0
    assert metrics["brier_score"] < 0.05
    assert metrics["ece_calibration_error"] < 0.15
    assert "roc_auc_delta" in res["baseline_comparison"]


def test_4_experiment_manifest_registry():
    manifest = ModelManifest(
        model_id="exp_test_001",
        model_name="Test Benchmark Model",
        model_version="v1.0.0",
        model_type="risk",
        dataset_id="uci_credit_default",
        dataset_version="v1.0.0",
        feature_version="risk_v1.0.0",
        metrics={"roc_auc": 0.82},
        status="EXPERIMENTAL",
    )

    experiment_manifest_manager.register_manifest(manifest)
    retrieved = experiment_manifest_manager.get_manifest("exp_test_001")
    assert retrieved is not None
    assert retrieved.model_name == "Test Benchmark Model"
    assert retrieved.status == "EXPERIMENTAL"


def test_5_offline_risk_training_experiment():
    manifest = run_credit_risk_training_experiment(dataset_id="uci_credit_default", random_seed=42)
    assert isinstance(manifest, ModelManifest)
    assert manifest.status == "EXPERIMENTAL"
    assert "roc_auc" in manifest.metrics
    assert manifest.metrics["roc_auc"] >= 0.70


def test_6_offline_fraud_training_experiment():
    manifest = run_fraud_aml_training_experiment(dataset_id="ibm_aml_synthetic", random_seed=42)
    assert isinstance(manifest, ModelManifest)
    assert manifest.status == "EXPERIMENTAL"
    assert "pr_auc" in manifest.metrics


def test_7_offline_anomaly_training_experiment():
    manifest = run_transaction_anomaly_training_experiment(random_seed=42)
    assert isinstance(manifest, ModelManifest)
    assert manifest.model_type == "anomaly"
