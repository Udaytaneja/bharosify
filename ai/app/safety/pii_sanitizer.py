import re
from typing import Dict, List, Tuple



class PIISanitizer:
    """
    Detects and sanitizes PII identifiers (PAN, Aadhaar, SSN, Credit Cards, Phone numbers, Email)
    before LLM calls and in model outputs.
    """

    # RegEx Patterns for PII
    PAN_PATTERN = re.compile(r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b', re.IGNORECASE)
    AADHAAR_PATTERN = re.compile(r'\b[2-9]{1}[0-9]{3}\s?[0-9]{4}\s?[0-9]{4}\b')
    SSN_PATTERN = re.compile(r'\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b')
    CREDIT_CARD_PATTERN = re.compile(r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b')
    PHONE_PATTERN = re.compile(r'\b(?:\+91[\-\s]?)?[6-9]\d{9}\b')
    EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

    def sanitize(self, text: str) -> Tuple[str, bool, Dict[str, str]]:
        """
        Redacts PII from text input.
        Returns:
            Tuple[sanitized_text, was_redacted, replacement_map]
        """
        replacement_map: Dict[str, str] = {}
        redacted = False

        def make_replacer(label: str):
            def replacer(match):
                nonlocal redacted
                redacted = True
                token = f"[REDACTED_{label}_{len(replacement_map)+1}]"
                replacement_map[token] = match.group(0)
                return token
            return replacer

        sanitized_text = self.PAN_PATTERN.sub(make_replacer("PAN"), text)
        sanitized_text = self.AADHAAR_PATTERN.sub(make_replacer("AADHAAR"), sanitized_text)
        sanitized_text = self.SSN_PATTERN.sub(make_replacer("SSN"), sanitized_text)
        sanitized_text = self.CREDIT_CARD_PATTERN.sub(make_replacer("CREDIT_CARD"), sanitized_text)

        return sanitized_text, redacted, replacement_map


class SecretDetector:
    """
    Detects and blocks leakage of confidential credentials, JWT tokens, API keys, and connection strings.
    """

    SECRET_PATTERNS = [
        ("JWT_TOKEN", re.compile(r'\beyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*\b')),
        ("API_KEY", re.compile(r'\b(?:sk|sec|api_key)_[a-zA-Z0-9]{20,}\b', re.IGNORECASE)),
        ("BEARER_TOKEN", re.compile(r'\bBearer\s+[A-Za-z0-9\-._~+/]+=*\b', re.IGNORECASE)),
        ("DB_CONNECTION_URI", re.compile(r'\b(?:postgresql|mysql|sqlite|mongodb)\:\/\/[^\s]+\b', re.IGNORECASE)),
        ("PRIVATE_KEY", re.compile(r'-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----', re.IGNORECASE)),
        ("HARDCODED_PASSWORD", re.compile(r'(?:password|passwd|secret)\s*[:=]\s*["\']?[^\s"\'\`]{6,}["\']?', re.IGNORECASE)),
    ]

    def detect_and_redact(self, text: str) -> Tuple[str, bool, List[str]]:
        """
        Detects and redacts secrets in input or output text.
        Returns:
            Tuple[cleaned_text, secrets_found_bool, detected_secret_labels]
        """
        detected_labels = []
        cleaned_text = text

        for label, pattern in self.SECRET_PATTERNS:
            if pattern.search(cleaned_text):
                detected_labels.append(label)
                cleaned_text = pattern.sub(f"[REDACTED_SECRET_{label}]", cleaned_text)

        return cleaned_text, len(detected_labels) > 0, detected_labels


pii_sanitizer = PIISanitizer()
secret_detector = SecretDetector()
