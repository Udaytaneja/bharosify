from typing import List, Dict, Any, Tuple
from ai.app.perception.tampering import DocumentAnomaly


class ConfidenceScorer:
    """
    Computes overall document confidence score and enforces review routing rules.
    CRITICAL RULE: Successful OCR text extraction DOES NOT EQUAL AUTHENTICITY.
    """

    CONFIDENCE_THRESHOLD = 0.85

    def evaluate(
        self,
        classification_confidence: float,
        ocr_confidence: float,
        layout_confidence: float,
        anomalies: List[DocumentAnomaly],
        extracted_fields: Dict[str, Any],
    ) -> Tuple[float, bool, List[str]]:
        """
        Calculates overall document confidence and determines if human banker review is required.
        Returns:
            Tuple[overall_confidence, requires_review, review_reasons]
        """
        # Weighted overall confidence formula
        weighted_score = (
            (classification_confidence * 0.25) +
            (ocr_confidence * 0.40) +
            (layout_confidence * 0.35)
        )

        requires_review = False
        review_reasons: List[str] = []

        # Rule 1: High severity or critical tampering anomalies force review
        high_severity_anomalies = [a for a in anomalies if a.severity in ["high", "critical"]]
        if high_severity_anomalies:
            requires_review = True
            for a in high_severity_anomalies:
                review_reasons.append(f"Tampering Anomaly Detected [{a.anomaly_type}]: {a.description}")
            # Penalize confidence score for tampering
            weighted_score -= (0.25 * len(high_severity_anomalies))

        # Rule 2: Low extraction confidence forces review
        if weighted_score < self.CONFIDENCE_THRESHOLD:
            requires_review = True
            review_reasons.append(
                f"Overall document extraction confidence ({round(weighted_score, 2)}) is below threshold ({self.CONFIDENCE_THRESHOLD})"
            )

        # Rule 3: Missing essential fields for the document type forces review
        if not extracted_fields or len(extracted_fields) < 2:
            requires_review = True
            review_reasons.append("Fewer than 2 essential fields could be parsed from the document")

        final_confidence = max(0.0, min(1.0, round(weighted_score, 2)))

        # Rule 4: Mandatory authenticity disclaimer (OCR success != Authenticity)
        review_reasons.append(
            "Authenticity Note: Successful OCR extraction does not certify document authenticity. Verification against authoritative bank ledgers required."
        )

        return final_confidence, requires_review, review_reasons


confidence_scorer = ConfidenceScorer()
