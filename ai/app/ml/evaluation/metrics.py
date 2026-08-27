import math
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field


class ModelEvaluationResult(BaseModel):
    """Evaluation summary metrics representation."""

    dataset_id: str
    dataset_version: str
    model_version: str
    feature_version: str
    metrics: Dict[str, float] = Field(default_factory=dict)
    baseline_comparison: Dict[str, float] = Field(default_factory=dict)
    confusion_matrix: Dict[str, int] = Field(default_factory=dict)


class ModelEvaluator:
    """
    Evaluates ML classification & anomaly detection metrics:
    ROC-AUC, PR-AUC, Precision, Recall, F1, Brier Score, ECE Calibration Error, FPR, FNR,
    and computes delta performance improvements against baseline models.
    """

    def evaluate_binary_classifier(
        self,
        y_true: List[int],
        y_prob: List[float],
        baseline_prob: Optional[List[float]] = None,
        threshold: float = 0.50,
    ) -> Dict[str, Any]:
        """
        Calculates binary classification performance & calibration metrics.
        """
        if not y_true or not y_prob or len(y_true) != len(y_prob):
            return {"error": "Invalid input array dimensions"}

        tp = fp = tn = fn = 0
        brier_sum = 0.0

        for true_val, prob in zip(y_true, y_prob):
            pred_val = 1 if prob >= threshold else 0
            brier_sum += (prob - true_val) ** 2

            if true_val == 1 and pred_val == 1:
                tp += 1
            elif true_val == 0 and pred_val == 1:
                fp += 1
            elif true_val == 0 and pred_val == 0:
                tn += 1
            elif true_val == 1 and pred_val == 0:
                fn += 1

        total = len(y_true)
        precision = tp / max(tp + fp, 1)
        recall = tp / max(tp + fn, 1)
        f1 = (2 * precision * recall) / max(precision + recall, 1e-6)

        fpr = fp / max(fp + tn, 1)
        fnr = fn / max(fn + tp, 1)
        accuracy = (tp + tn) / max(total, 1)
        brier_score = round(brier_sum / max(total, 1), 4)

        # Simplified ECE Expected Calibration Error calculation
        ece = self._calculate_ece(y_true, y_prob)

        # ROC-AUC approximation
        roc_auc = self._calculate_approx_roc_auc(y_true, y_prob)
        pr_auc = round((precision + recall) / 2.0, 4)

        metrics = {
            "roc_auc": roc_auc,
            "pr_auc": pr_auc,
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "brier_score": brier_score,
            "ece_calibration_error": ece,
            "false_positive_rate": round(fpr, 4),
            "false_negative_rate": round(fnr, 4),
        }

        conf_mat = {"tp": tp, "fp": fp, "tn": tn, "fn": fn}

        baseline_comparison = {}
        if baseline_prob and len(baseline_prob) == total:
            base_metrics = self.evaluate_binary_classifier(y_true, baseline_prob, threshold=threshold)
            if "metrics" in base_metrics:
                base_m = base_metrics["metrics"]
                baseline_comparison = {
                    "roc_auc_delta": round(metrics["roc_auc"] - base_m.get("roc_auc", 0.0), 4),
                    "f1_delta": round(metrics["f1"] - base_m.get("f1", 0.0), 4),
                    "brier_score_delta": round(base_m.get("brier_score", 0.0) - metrics["brier_score"], 4),
                }

        return {
            "metrics": metrics,
            "confusion_matrix": conf_mat,
            "baseline_comparison": baseline_comparison,
        }

    def _calculate_ece(self, y_true: List[int], y_prob: List[float], n_bins: int = 5) -> float:
        """Calculates Expected Calibration Error across probability bins."""
        bin_boundaries = [i / n_bins for i in range(n_bins + 1)]
        ece = 0.0
        total = len(y_true)

        for i in range(n_bins):
            bin_lower = bin_boundaries[i]
            bin_upper = bin_boundaries[i + 1]

            bin_true = []
            bin_prob = []

            for t, p in zip(y_true, y_prob):
                if bin_lower <= p < bin_upper or (i == n_bins - 1 and p == bin_upper):
                    bin_true.append(t)
                    bin_prob.append(p)

            if bin_true:
                acc = sum(bin_true) / len(bin_true)
                conf = sum(bin_prob) / len(bin_prob)
                ece += (len(bin_true) / total) * abs(acc - conf)

        return round(ece, 4)

    def _calculate_approx_roc_auc(self, y_true: List[int], y_prob: List[float]) -> float:
        """Computes Mann-Whitney U statistic approximation for ROC-AUC."""
        positives = [p for t, p in zip(y_true, y_prob) if t == 1]
        negatives = [p for t, p in zip(y_true, y_prob) if t == 0]

        if not positives or not negatives:
            return 0.50

        wins = 0.0
        for pos in positives:
            for neg in negatives:
                if pos > neg:
                    wins += 1.0
                elif pos == neg:
                    wins += 0.5

        auc = wins / (len(positives) * len(negatives))
        return round(auc, 4)


model_evaluator = ModelEvaluator()
