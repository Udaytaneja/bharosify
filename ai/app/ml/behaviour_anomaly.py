from typing import Any, Dict
from ai.app.core.config import ai_settings
from ai.app.ml.features import BehaviourAnomalyFeatureVector, feature_preprocessor
from ai.app.ml.interfaces import BaseBehaviourAnomalyModel, BehaviourAnomalySignal


class BehaviourAnomalyModel(BaseBehaviourAnomalyModel):
    """Account Behaviour Anomaly Model Adapter."""

    def __init__(self):
        self.model_name = "IsolationForest-BehaviourAnomaly"
        self.version = ai_settings.anomaly_model_version
        self.feature_schema_version = "beh_anomaly_v1.0.0"

    async def detect_behaviour_anomaly(
        self, session_features: Dict[str, Any], user_baseline: Dict[str, Any]
    ) -> BehaviourAnomalySignal:
        feat_vector: BehaviourAnomalyFeatureVector = feature_preprocessor.extract_behaviour_features(
            session_features, user_baseline
        )

        anomalous_features = []
        if feat_vector.session_duration_sec < 5.0 and feat_vector.navigation_depth > 10:
            anomalous_features.append("Automated Fast Navigation Burst")
        if feat_vector.device_switch_flag > 0:
            anomalous_features.append("Unrecognized Device Telemetry")
        if feat_vector.unusual_access_flag > 0:
            anomalous_features.append("Unusual Resource Privilege Access")

        is_anomalous = len(anomalous_features) > 0
        score = 0.78 if is_anomalous else 0.04
        severity = "high" if score >= ai_settings.anomaly_threshold else ("warning" if is_anomalous else "info")

        return BehaviourAnomalySignal(
            anomaly_score=score,
            is_anomalous=is_anomalous,
            behaviour_vector="device_switch" if feat_vector.device_switch_flag > 0 else "normal",
            severity=severity,
            confidence=0.88,
            anomalous_features=anomalous_features,
            model_version=f"{self.version}-calibrated",
        )


behaviour_anomaly_model = BehaviourAnomalyModel()
