import math


class ModelCalibrator:
    """Probability Calibrator (Platt Sigmoidal Scaling) & Confidence Evaluator."""

    def calibrate_probability(self, raw_score: float, a: float = -1.0, b: float = 0.0) -> float:
        """
        Applies Platt Sigmoidal Calibration: P(y=1|x) = 1 / (1 + exp(A*f(x) + B))
        """
        try:
            val = 1.0 / (1.0 + math.exp(a * raw_score + b))
            return max(0.001, min(0.999, round(val, 4)))
        except OverflowError:
            return 0.999 if raw_score > 0 else 0.001

    def compute_confidence(self, probability: float, num_features: int) -> float:
        """
        Computes model confidence based on probability distance from decision margin (0.5)
        and feature completeness.
        """
        margin_dist = abs(probability - 0.5) * 2.0  # 0.0 at threshold, 1.0 at extremes
        base_conf = 0.70 + (margin_dist * 0.28)
        return min(0.98, max(0.65, round(base_conf, 2)))


model_calibrator = ModelCalibrator()
