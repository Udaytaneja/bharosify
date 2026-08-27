import re
from typing import List, Tuple
from ai.app.core.exceptions import SafetyViolationError


class PromptShield:
    """Detects direct prompt injection attempts and system prompt overrides."""

    INJECTION_PATTERNS = [
        re.compile(r'ignore\s+(all\s+)?(previous\s+)?instructions', re.IGNORECASE),
        re.compile(r'you\s+are\s+now\s+in\s+developer\s+mode', re.IGNORECASE),
        re.compile(r'system\s+prompt\s+override', re.IGNORECASE),
        re.compile(r'bypass\s+(all\s+)?(policy|policies|rules|safety|guardrails)', re.IGNORECASE),
        re.compile(r'grant\s+me\s+admin', re.IGNORECASE),
        re.compile(r'approve\s+my\s+loan\s+automatically', re.IGNORECASE),
        re.compile(r'transfer\s+\$?[0-9,]+\s+to', re.IGNORECASE),
        re.compile(r'jailbreak', re.IGNORECASE),
        re.compile(r'reveal\s+(system\s+prompt|secret|api\s+key|password)', re.IGNORECASE),
        re.compile(r'do\s+anything\s+now', re.IGNORECASE),
        re.compile(r'exfiltrate\s+data', re.IGNORECASE),
    ]

    def validate(self, text: str) -> Tuple[bool, str]:
        """
        Validates text input for direct injection attempts.
        Returns:
            Tuple[is_safe, violation_reason]
        """
        for pattern in self.INJECTION_PATTERNS:
            if pattern.search(text):
                return False, f"Malicious input detected matching pattern: {pattern.pattern}"
        return True, ""


class IndirectInjectionScanner:
    """Scans parsed document text and retrieved RAG context chunks for embedded prompt injections."""

    INDIRECT_PATTERNS = [
        re.compile(r'\[\s*system\s*instruction\s*:\s*ignore', re.IGNORECASE),
        re.compile(r'<\s*system_override\s*>', re.IGNORECASE),
        re.compile(r'forget\s+all\s+prior\s+context', re.IGNORECASE),
        re.compile(r'assistant\s+must\s+output\s+the\s+following', re.IGNORECASE),
        re.compile(r'hidden\s+instruction\s*:', re.IGNORECASE),
        re.compile(r'override\s+financial\s+calculation', re.IGNORECASE),
        re.compile(r'send\s+all\s+data\s+to', re.IGNORECASE),
    ]

    def scan_chunk(self, chunk_text: str, source_name: str = "RAG Context") -> Tuple[bool, str]:
        """
        Scans a text chunk for indirect prompt injection vectors.
        """
        for pattern in self.INDIRECT_PATTERNS:
            if pattern.search(chunk_text):
                return False, f"Indirect prompt injection detected in '{source_name}': matches {pattern.pattern}"
        return True, ""


class MaliciousDocumentScanner:
    """Scans uploaded files and document content for malicious script payloads, shell commands, or obfuscated code."""

    MALICIOUS_PATTERNS = [
        re.compile(r'<\s*script\b', re.IGNORECASE),
        re.compile(r'javascript\s*:', re.IGNORECASE),
        re.compile(r'\beval\s*\(', re.IGNORECASE),
        re.compile(r'\bexec\s*\(', re.IGNORECASE),
        re.compile(r'powershell\s+-enc', re.IGNORECASE),
        re.compile(r'rm\s+-rf\s+/', re.IGNORECASE),
        re.compile(r'drop\s+database', re.IGNORECASE),
        re.compile(r'select\s+.*\s+from\s+information_schema', re.IGNORECASE),
    ]

    def scan_document(self, text_content: str, filename: str = "document") -> Tuple[bool, str]:
        """
        Scans document content for malicious code/scripts.
        """
        for pattern in self.MALICIOUS_PATTERNS:
            if pattern.search(text_content):
                return False, f"Malicious document content detected in '{filename}': matches {pattern.pattern}"
        return True, ""


prompt_shield = PromptShield()
indirect_injection_scanner = IndirectInjectionScanner()
malicious_doc_scanner = MaliciousDocumentScanner()
