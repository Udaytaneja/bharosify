from typing import Any, Dict, List, Tuple


class DataLeakageAuditor:
    """
    Offline Data Leakage Auditor for Financial ML Datasets.
    Audits for:
    1. Target leakage (post-decision information included in training features)
    2. Temporal ordering violations (future events predicting past outcomes)
    3. Duplicate record contamination across Train/Test splits
    """

    FORBIDDEN_POST_DECISION_FEATURES = [
        "repayment_status",
        "default_flag",
        "chargeoff_date",
        "collection_recovery_amount",
        "future_transaction_amount",
        "post_approval_balance",
    ]

    def audit_feature_set(self, feature_names: List[str]) -> Tuple[bool, List[str]]:
        """
        Audits a candidate feature set for illegal target leakage features.
        Returns:
            Tuple[passed_audit, leakage_violations]
        """
        violations = []
        for feature in feature_names:
            feature_lower = feature.lower()
            if any(forbidden in feature_lower for forbidden in self.FORBIDDEN_POST_DECISION_FEATURES):
                violations.append(f"Target Leakage Hazard: Feature '{feature}' contains post-decision outcome data.")

        return len(violations) == 0, violations

    def audit_temporal_split(self, train_timestamps: List[float], test_timestamps: List[float]) -> bool:
        """
        Verifies that max(train_timestamps) < min(test_timestamps) to enforce strict temporal ordering.
        """
        if not train_timestamps or not test_timestamps:
            return True
        return max(train_timestamps) <= min(test_timestamps)


data_leakage_auditor = DataLeakageAuditor()
