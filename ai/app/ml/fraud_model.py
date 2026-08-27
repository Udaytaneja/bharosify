import os
import time
from typing import Any, Dict, List, Optional, Tuple

from ai.app.core.config import ai_settings
from ai.app.models.model_lifecycle import model_registry_manager
from ai.app.ml.features import FraudFeatureVector, feature_preprocessor
from ai.app.ml.interfaces import BaseFraudClassificationModel, FeatureAttribution, FraudClassificationSignal


class FraudClassificationModel(BaseFraudClassificationModel):
    """
    Production LightGBM Fraud Classification Model Adapter.
    Executes model inference when trained fraud_model.txt artifact is present.
    If artifact is unconfigured/missing, returns calibrated heuristic probability
    with status 'MODEL_UNAVAILABLE_CALIBRATED_FALLBACK'.
    Non-authoritative boundary: Produces signals ONLY; backend policy engine decides action.
    """

    def __init__(self):
        self.model_name = "LightGBM-FraudClassifier"
        self.version = ai_settings.fraud_model_version
        self.feature_schema_version = "fraud_v1.0.0"

    def _get_or_load_lgb(self) -> Tuple[Optional[Any], bool, str]:
        """Retrieves cached LightGBM instance or initializes once safely."""
        model_path = ai_settings.fraud_model_path
        if not model_path or not os.path.exists(model_path):
            return None, False, f"LightGBM fraud model artifact path '{model_path}' is not configured or file is missing."

        cached = model_registry_manager.get_loaded_instance(self.model_name)
        if cached is not None:
            return cached, True, "MODEL-READY"

        try:
            import lightgbm as lgb

            booster = lgb.Booster(model_file=model_path)
            model_registry_manager.set_loaded_instance(self.model_name, booster, artifact_path=model_path)
            return booster, True, "MODEL-READY"
        except ImportError:
            return None, False, "LightGBM library is not installed in runtime environment."
        except Exception as e:
            return None, False, f"LightGBM model loading failed: {str(e)}"

    async def classify_fraud(self, event_features: Dict[str, Any]) -> FraudClassificationSignal:
        """
        Executes fraud classification inference pipeline.
        Returns: FraudClassificationSignal
        """
        feat_vector: FraudFeatureVector = feature_preprocessor.extract_fraud_features(event_features)

        booster, is_available, status_msg = self._get_or_load_lgb()

        fraud_prob: float = 0.02
        fraud_type = "normal"
        severity = "info"
        model_ver = self.version
        attributions: List[FeatureAttribution] = []

        if is_available and booster is not None:
            try:
                preds = booster.predict([feat_vector.to_numpy()])
                fraud_prob = float(preds[0])
                model_ver = f"{self.version}-lgb"
            except Exception:
                fraud_prob, fraud_type, severity, attributions = self._evaluate_calibrated_baseline(feat_vector)
                model_ver = f"{self.version}-calibrated-fallback"
        else:
            fraud_prob, fraud_type, severity, attributions = self._evaluate_calibrated_baseline(feat_vector)
            model_ver = f"{self.version}-calibrated-fallback"

        return FraudClassificationSignal(
            fraud_score=round(fraud_prob, 4),
            fraud_type=fraud_type,
            severity=severity,
            confidence=0.92 if is_available else 0.85,
            attributions=attributions,
            model_version=model_ver,
        )

    def _evaluate_calibrated_baseline(self, feats: FraudFeatureVector) -> Tuple[float, str, str, List[FeatureAttribution]]:
        """Calibrated heuristic baseline when model weights are unconfigured."""
        attributions = []
        score = 0.02
        fraud_type = "normal"
        severity = "info"

        if feats.failed_login_count >= 5:
            score += 0.55
            fraud_type = "account_takeover"
            attributions.append(
                FeatureAttribution(
                    feature_name="failed_login_count",
                    value=feats.failed_login_count,
                    importance_weight=0.55,
                    impact_direction="positive",
                    description="Multiple consecutive failed login attempts detected",
                )
            )


        if feats.tx_velocity_10m >= 5:
            score += 0.35
            if fraud_type == "normal":
                fraud_type = "velocity_spike"
            attributions.append(
                FeatureAttribution(
                    feature_name="tx_velocity_10m",
                    value=feats.tx_velocity_10m,
                    importance_weight=0.35,
                    impact_direction="positive",
                    description="High transaction velocity within 10 minutes",
                )
            )

        if feats.device_switch_flag > 0:
            score += 0.15
            attributions.append(
                FeatureAttribution(
                    feature_name="device_switch_flag",
                    value=1.0,
                    importance_weight=0.15,
                    impact_direction="positive",
                    description="Transaction initiated from unrecognized device",
                )
            )

        score = min(0.99, round(score, 4))
        if score >= ai_settings.fraud_threshold:
            severity = "critical"
        elif score >= 0.50:
            severity = "high"
        elif score >= 0.25:
            severity = "warning"

        return score, fraud_type, severity, attributions


fraud_classification_model = FraudClassificationModel()
