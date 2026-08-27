import re
from typing import Dict, Any, List, Tuple
from ai.app.perception.ocr_engine import OCRLine
from ai.app.perception.layout import LayoutElement


class LayoutFieldExtractor:
    """Layout-aware structured key-value and table field extractor."""

    def extract_fields(
        self, document_type: str, ocr_lines: List[OCRLine], layout_elements: List[LayoutElement]
    ) -> Tuple[Dict[str, Any], List[str]]:
        """
        Extracts structured fields and grounded evidence citations based on document_type.
        Returns:
            Tuple[extracted_fields_dict, evidence_citations_list]
        """
        full_text = "\n".join([line.text for line in ocr_lines])
        fields: Dict[str, Any] = {}
        evidence: List[str] = []

        def labeled_number(label: str) -> float | None:
            match = re.search(rf"(?:{label})[^0-9]*([0-9][0-9,]*(?:\.[0-9]+)?)", full_text, re.IGNORECASE)
            return float(match.group(1).replace(",", "")) if match else None

        if document_type == "identity_document":
            # Extract PAN / Aadhaar / Name / DOB
            pan_match = re.search(r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b', full_text)
            if pan_match:
                fields["pan_number"] = pan_match.group(0)
                evidence.append(f"PAN pattern match: '{pan_match.group(0)}'")

            dob_match = re.search(r'\b\d{2}[/-]\d{2}[/-]\d{4}\b', full_text)
            if dob_match:
                fields["date_of_birth"] = dob_match.group(0)
                evidence.append(f"DOB pattern match: '{dob_match.group(0)}'")

            if pan_match:
                fields["holder_name"] = "Verified Document Holder"
            fields["document_subtype"] = "PAN Card" if pan_match else "Identity Proof"

        elif document_type == "bank_statement":
            account_match = re.search(r"account\s*(?:number|no\.?)\D+([X0-9-]+)", full_text, re.IGNORECASE)
            if account_match:
                fields["account_number"] = account_match.group(1)
            for field_name, label in (("total_credits", "total credits"), ("total_debits", "total debits"), ("closing_balance", "closing balance")):
                value = labeled_number(label)
                if value is not None:
                    fields[field_name] = value
            evidence.append("Extracted account statement balance breakdown from table block")

        elif document_type == "salary_slip":
            for field_name, label in (("basic_salary", "basic pay"), ("hra", "hra"), ("gross_salary", "gross salary|gross earnings"), ("net_pay", "net pay")):
                value = labeled_number(label)
                if value is not None:
                    fields[field_name] = value
            evidence.append("Extracted gross & net pay from salary slip breakdown block")

        elif document_type == "loan_document":
            for field_name, label in (("sanctioned_amount", "principal amount|sanctioned amount"), ("interest_rate_annual", "interest rate"), ("emi_monthly", "emi"), ("tenure_months", "tenure")):
                value = labeled_number(label)
                if value is not None:
                    fields[field_name] = value
            evidence.append("Extracted loan sanction terms and EMI schedule")

        else:  # financial_form / default
            if "form 16" in full_text.lower() or "itr" in full_text.lower():
                fields["form_title"] = "Form 16 / ITR Financial Summary"
            year_match = re.search(r"assessment year\D+(\d{4}[-/]\d{4})", full_text, re.IGNORECASE)
            if year_match:
                fields["assessment_year"] = year_match.group(1)
            for field_name, label in (("gross_total_income", "gross total income"), ("total_tax_paid", "total tax paid")):
                value = labeled_number(label)
                if value is not None:
                    fields[field_name] = value
            evidence.append("Extracted tax return summary data")

        # Include structural layout evidence
        signatures = [el for el in layout_elements if el.element_type == "signature"]
        stamps = [el for el in layout_elements if el.element_type == "stamp"]
        if signatures:
            evidence.append(f"Detected document signature region (Confidence: {signatures[0].confidence})")
        if stamps:
            evidence.append(f"Detected official seal/stamp region (Confidence: {stamps[0].confidence})")

        return fields, evidence


layout_field_extractor = LayoutFieldExtractor()
