from typing import Dict, List
from ai.app.ml.interfaces import FeatureAttribution


class SHAPAttributor:
    """Computes SHAP-like feature importance attributions for model explainability."""

    def compute_risk_attributions(self, features: Dict[str, float]) -> List[FeatureAttribution]:
        attributions = []

        dti = features.get("dti_ratio", 0.4)
        if dti > 0.5:
            attributions.append(
                FeatureAttribution(
                    feature_name="dti_ratio",
                    value=dti,
                    importance_weight=0.35,
                    impact_direction="negative",
                    description=f"High Debt-to-Income ratio ({round(dti*100, 1)}%) increases credit default risk.",
                )
            )
        else:
            attributions.append(
                FeatureAttribution(
                    feature_name="dti_ratio",
                    value=dti,
                    importance_weight=0.25,
                    impact_direction="positive",
                    description=f"Healthy Debt-to-Income ratio ({round(dti*100, 1)}%) supports creditworthiness.",
                )
            )

        past_delinq = features.get("past_delinquencies", 0.0)
        if past_delinq > 0:
            attributions.append(
                FeatureAttribution(
                    feature_name="past_delinquencies",
                    value=past_delinq,
                    importance_weight=0.40,
                    impact_direction="negative",
                    description=f"Recorded {int(past_delinq)} past payment delinquencies.",
                )
            )
        else:
            attributions.append(
                FeatureAttribution(
                    feature_name="past_delinquencies",
                    value=0.0,
                    importance_weight=0.20,
                    impact_direction="positive",
                    description="Clean repayment history with zero delinquencies.",
                )
            )

        account_age = features.get("account_age_months", 12.0)
        if account_age >= 24:
            attributions.append(
                FeatureAttribution(
                    feature_name="account_age_months",
                    value=account_age,
                    importance_weight=0.15,
                    impact_direction="positive",
                    description=f"Established account history of {int(account_age)} months.",
                )
            )

        return attributions

    def explain_risk_prediction(self, features: Dict[str, float]) -> List[FeatureAttribution]:
        return self.compute_risk_attributions(features)



shap_attributor = SHAPAttributor()
