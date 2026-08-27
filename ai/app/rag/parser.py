from typing import Dict, Any, Tuple


class DocumentParser:
    """Parses authorized financial policies, product rules, compliance documents, and customer records."""

    SUPPORTED_TYPES = {
        "bank_policy",
        "product_rule",
        "governance_policy",
        "agent_policy",
        "compliance",
        "financial_document",
    }

    def parse(self, text_content: str, document_type: str, document_id: str) -> Tuple[str, Dict[str, Any]]:
        """
        Parses document text content.
        Returns:
            Tuple[clean_text, document_metadata]
        """
        if document_type not in self.SUPPORTED_TYPES:
            document_type = "bank_policy"

        clean_text = text_content.strip()
        doc_meta = {
            "document_id": document_id,
            "document_type": document_type,
            "character_count": len(clean_text),
        }
        return clean_text, doc_meta


document_parser = DocumentParser()
