from typing import Tuple, Dict, Any


class DocumentClassifier:
    """Classifies financial document types based on text patterns and structural features."""

    DOCUMENT_TYPES = {
        "identity_document": ["pan", "aadhaar", "passport", "voter id", "driving license", "identity", "dob", "government of india"],
        "bank_statement": ["bank statement", "account statement", "closing balance", "opening balance", "credit", "debit", "ifsc", "branch"],
        "salary_slip": ["salary slip", "pay slip", "basic pay", "hra", "pf contribution", "net pay", "gross earnings", "deductions"],
        "loan_document": ["loan agreement", "sanction letter", "principal amount", "interest rate", "emi", "tenure", "borrower", "lender"],
        "financial_form": ["form 16", "itr", "tax return", "assessment year", "gross total income", "financial form"],
    }

    def classify(self, text_content: str, file_name: str) -> Tuple[str, float, Dict[str, Any]]:
        """
        Classifies document content into one of the initial supported document types.
        Returns:
            Tuple[document_type, confidence_score, metadata]
        """
        combined_text = f"{file_name} {text_content}".lower()
        scores = {}

        for doc_type, keywords in self.DOCUMENT_TYPES.items():
            matches = sum(1 for kw in keywords if kw in combined_text)
            scores[doc_type] = matches / len(keywords)

        best_type = max(scores, key=scores.get)
        highest_score = scores[best_type]

        if highest_score == 0.0:
            # Default fallback for unclassified documents
            best_type = "financial_form"
            confidence = 0.60
        else:
            confidence = min(0.98, 0.70 + (highest_score * 0.30))

        metadata = {
            "all_scores": scores,
            "matched_type": best_type,
            "classifier_version": "v1.0.0",
        }
        return best_type, round(confidence, 2), metadata


document_classifier = DocumentClassifier()
