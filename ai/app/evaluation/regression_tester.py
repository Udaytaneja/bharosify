from typing import Any, Dict, List, Tuple


class RegressionTester:
    """
    Automated Regression Test Runner.
    Compares candidate LLM / prompt evaluation runs against production baseline runs
    to prevent silent performance degradation.
    """

    def compare_runs(
        self, candidate_result: Dict[str, Any], baseline_result: Dict[str, Any]
    ) -> Tuple[bool, List[str], Dict[str, Any]]:
        """
        Compares candidate vs baseline metrics for performance regression.
        Returns:
            Tuple[is_regression_free, regression_reasons, comparison_summary]
        """
        cand_m = candidate_result.get("metrics", {})
        base_m = baseline_result.get("metrics", {})
        reasons = []

        # Accuracy check
        cand_acc = cand_m.get("accuracy", 0.0)
        base_acc = base_m.get("accuracy", 0.0)
        if cand_acc < (base_acc - 2.0):
            reasons.append(f"Accuracy regression: candidate accuracy {cand_acc}% dropped >2% compared to baseline {base_acc}%")

        # F1 Score check
        cand_f1 = cand_m.get("f1", 0.0)
        base_f1 = base_m.get("f1", 0.0)
        if cand_f1 < (base_f1 - 0.03):
            reasons.append(f"F1 score regression: candidate F1 {cand_f1} dropped >0.03 compared to baseline {base_f1}")

        # Hallucination check
        cand_hal = cand_m.get("hallucination_rate", 0.0)
        base_hal = base_m.get("hallucination_rate", 0.0)
        if cand_hal > (base_hal + 1.0):
            reasons.append(f"Hallucination rate regression: candidate {cand_hal}% increased >1% compared to baseline {base_hal}%")

        # Security failure check
        cand_sec = cand_m.get("security_failures", 0.0)
        base_sec = base_m.get("security_failures", 0.0)
        if cand_sec > base_sec:
            reasons.append(f"Security regression: candidate security failure rate {cand_sec}% is worse than baseline {base_sec}%")

        is_regression_free = len(reasons) == 0

        summary = {
            "status": "REGRESSION_PASS" if is_regression_free else "REGRESSION_FAILURE",
            "is_regression_free": is_regression_free,
            "reasons": reasons,
            "candidate_metrics": cand_m,
            "baseline_metrics": base_m,
        }

        return is_regression_free, reasons, summary


regression_tester = RegressionTester()
