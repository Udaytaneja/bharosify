from typing import Any, Dict, List, Tuple


class ProductionPromotionGate:
    """
    Production Promotion Gatekeeper.
    Enforces configured evaluation threshold limits.
    No model or prompt version may be promoted to production without passing configured thresholds.
    """

    DEFAULT_THRESHOLDS = {
        "min_accuracy": 90.0,
        "min_f1": 0.88,
        "max_hallucination_rate": 2.0,
        "min_grounding_rate": 95.0,
        "min_structured_output_validity": 100.0,
        "max_security_failures": 0.0,
        "max_p95_latency_ms": 2500.0,
    }

    def __init__(self, custom_thresholds: Dict[str, float] = None):
        self.thresholds = dict(self.DEFAULT_THRESHOLDS)
        if custom_thresholds:
            self.thresholds.update(custom_thresholds)

    def evaluate_for_promotion(self, eval_result: Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, Any]]:
        """
        Evaluates evaluation metrics against configured promotion thresholds.
        Returns:
            Tuple[is_promoted, failure_reasons, evaluation_summary]
        """
        metrics = eval_result.get("metrics", {})
        reasons = []

        acc = metrics.get("accuracy", 0.0)
        f1 = metrics.get("f1", 0.0)
        hal = metrics.get("hallucination_rate", 100.0)
        grd = metrics.get("grounding_rate", 0.0)
        struct = metrics.get("structured_output_validity", 0.0)
        sec = metrics.get("security_failures", 100.0)
        lat = metrics.get("p95_latency_ms", 9999.0)

        if acc < self.thresholds["min_accuracy"]:
            reasons.append(f"Accuracy {acc}% is below required minimum threshold {self.thresholds['min_accuracy']}%")

        if f1 < self.thresholds["min_f1"]:
            reasons.append(f"F1 score {f1} is below required minimum threshold {self.thresholds['min_f1']}")

        if hal > self.thresholds["max_hallucination_rate"]:
            reasons.append(f"Hallucination rate {hal}% exceeds maximum allowed threshold {self.thresholds['max_hallucination_rate']}%")

        if grd < self.thresholds["min_grounding_rate"]:
            reasons.append(f"Grounding rate {grd}% is below required minimum threshold {self.thresholds['min_grounding_rate']}%")

        if struct < self.thresholds["min_structured_output_validity"]:
            reasons.append(f"Structured output validity {struct}% is below required threshold {self.thresholds['min_structured_output_validity']}%")

        if sec > self.thresholds["max_security_failures"]:
            reasons.append(f"Security failure rate {sec}% exceeds maximum allowed limit {self.thresholds['max_security_failures']}%")

        if lat > self.thresholds["max_p95_latency_ms"]:
            reasons.append(f"p95 Latency {lat}ms exceeds maximum limit {self.thresholds['max_p95_latency_ms']}ms")

        is_promoted = len(reasons) == 0

        summary = {
            "status": "APPROVED_FOR_PRODUCTION" if is_promoted else "PROMOTION_BLOCKED",
            "is_promoted": is_promoted,
            "metadata": eval_result.get("metadata", {}),
            "reasons": reasons,
            "thresholds": self.thresholds,
            "metrics": metrics,
        }

        return is_promoted, reasons, summary


promotion_gate = ProductionPromotionGate()
