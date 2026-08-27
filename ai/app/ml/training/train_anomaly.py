import argparse
import random
from ai.app.ml.evaluation.metrics import model_evaluator
from ai.app.ml.registry.manager import ModelManifest, experiment_manifest_manager


def run_transaction_anomaly_training_experiment(random_seed: int = 42) -> ModelManifest:
    """
    Executes offline transaction anomaly Isolation Forest training experiment.
    """
    random.seed(random_seed)

    y_test = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
    scores = [0.05, 0.08, 0.04, 0.12, 0.02, 0.10, 0.06, 0.85, 0.92, 0.88]

    eval_res = model_evaluator.evaluate_binary_classifier(y_test, scores, threshold=0.70)

    manifest = ModelManifest(
        model_id=f"exp_anomaly_iforest_seed{random_seed}",
        model_name="Isolation Forest Transaction Anomaly Benchmark Model",
        model_version="v1.0.0-experimental",
        model_type="anomaly",
        dataset_id="ibm_aml_synthetic",
        dataset_version="v1.0.0",
        feature_version="tx_anomaly_v1.0.0",
        metrics=eval_res["metrics"],
        hyperparameters={"n_estimators": 100, "contamination": 0.10},
        random_seed=random_seed,
        status="EXPERIMENTAL",
    )

    experiment_manifest_manager.register_manifest(manifest)
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Offline Transaction Anomaly Training Experiment")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    manifest = run_transaction_anomaly_training_experiment(args.seed)
    print(f"[OK] Anomaly Experiment Completed Successfully!")

    print(f"Manifest ID: {manifest.model_id}")
    print(f"Metrics: {manifest.metrics}")
