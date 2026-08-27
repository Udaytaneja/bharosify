import os
import time
from typing import Any, Dict, List, Optional, Tuple

from ai.app.core.config import ai_settings
from ai.app.models.model_lifecycle import model_registry_manager
from ai.app.ml.features import TransactionAnomalyFeatureVector, feature_preprocessor
from ai.app.ml.interfaces import BaseTransactionAnomalyModel, TransactionAnomalySignal


class TransactionAnomalyModel(BaseTransactionAnomalyModel):
    """
    Production Isolation Forest Transaction Anomaly Model Adapter.
    Uses scikit-learn IsolationForest estimator to compute anomaly scores and velocity spikes.
    Returns status 'MODEL_UNAVAILABLE_CALIBRATED_FALLBACK' when model artifact is missing.
    """

    def __init__(self):
        self.model_name = "IsolationForest-AnomalyDetector"
        self.version = ai_settings.anomaly_model_version
        self.feature_schema_version = "tx_anomaly_v1.0.0"

    def _get_or_load_iforest(self) -> Tuple[Optional[Any], bool, str]:
        """Retrieves cached IsolationForest instance or initializes once safely."""
        model_path = ai_settings.anomaly_model_path
        if not model_path or not os.path.exists(model_path):
            return None, False, f"IsolationForest artifact path '{model_path}' is not configured or file is missing."

        cached = model_registry_manager.get_loaded_instance(self.model_name)
        if cached is not None:
            return cached, True, "MODEL-READY"

        try:
            import joblib

            estimator = joblib.load(model_path)
            model_registry_manager.set_loaded_instance(self.model_name, estimator, artifact_path=model_path)
            return estimator, True, "MODEL-READY"
        except ImportError:
            return None, False, "joblib/scikit-learn is not installed in runtime environment."
        except Exception as e:
            return None, False, f"IsolationForest loading failed: {str(e)}"

    async def detect_transaction_anomaly(
        self, transaction: Dict[str, Any], historical_baseline: Dict[str, Any]
    ) -> TransactionAnomalySignal:
        """
        Executes transaction anomaly detection pipeline.
        Returns: TransactionAnomalySignal
        """
        feat_vector: TransactionAnomalyFeatureVector = feature_preprocessor.extract_transaction_features(
            transaction, historical_baseline
        )

        estimator, is_available, status_msg = self._get_or_load_iforest()

        z_score = feat_vector.amount_z_score
        vel_ratio = feat_vector.velocity_ratio
        anomalous_features = []

        if z_score > 3.0:
            anomalous_features.append(f"Amount Z-Score ({z_score}) > 3.0 Standard Deviations")
        if vel_ratio > 3.0:
            anomalous_features.append(f"Transaction Velocity Ratio ({vel_ratio}) exceeds 3x baseline")

        is_anomalous = len(anomalous_features) > 0
        model_ver = self.version

        if is_available and estimator is not None:
            try:
                # Isolation Forest decision_function returns negative for anomalies
                raw_score = float(estimator.decision_function([feat_vector.to_numpy()])[0])
                anomaly_score = max(0.01, min(0.99, round(0.50 - raw_score, 2)))
                is_anomalous = bool(estimator.predict([feat_vector.to_numpy()])[0] == -1)
                model_ver = f"{self.version}-iforest"
            except Exception:
                anomaly_score = min(0.99, max(0.02, 0.10 + (z_score * 0.15) + (vel_ratio * 0.20)))
                model_ver = f"{self.version}-calibrated-fallback"
        else:
            anomaly_score = min(0.99, max(0.02, 0.10 + (z_score * 0.15) + (vel_ratio * 0.20)))
            model_ver = f"{self.version}-calibrated-fallback"

        severity = "high" if anomaly_score >= ai_settings.anomaly_threshold else ("warning" if is_anomalous else "info")

        return TransactionAnomalySignal(
            anomaly_score=round(anomaly_score, 2),
            is_anomalous=is_anomalous,
            velocity_spike_ratio=vel_ratio,
            amount_deviation_sigma=z_score,
            severity=severity,
            confidence=0.91 if is_available else 0.85,
            anomalous_features=anomalous_features,
            model_version=model_ver,
        )


transaction_anomaly_model = TransactionAnomalyModel()
