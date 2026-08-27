import re
from typing import List, Tuple
from ai.app.rag.schema import DocumentChunk


class ContextFilter:
    """Filters context and neutralizes Indirect Prompt Injection attacks in retrieved documents."""

    INDIRECT_INJECTION_PATTERNS = [
        re.compile(r'system\s+(prompt\s+)?override', re.IGNORECASE),
        re.compile(r'ignore\s+previous\s+instructions', re.IGNORECASE),
        re.compile(r'bypass\s+policy', re.IGNORECASE),
        re.compile(r'approve\s+loan\s+automatically', re.IGNORECASE),
        re.compile(r'grant\s+admin', re.IGNORECASE),
    ]

    def filter_and_sanitize(
        self, chunks_with_scores: List[Tuple[DocumentChunk, float]]
    ) -> Tuple[List[Tuple[DocumentChunk, float]], bool]:
        """
        Sanitizes retrieved text chunks against indirect prompt injection.
        Returns:
            Tuple[sanitized_chunks_with_scores, injection_detected_flag]
        """
        sanitized_list = []
        injection_detected = False

        for chunk, score in chunks_with_scores:
            text = chunk.text
            clean_text = text

            for pattern in self.INDIRECT_INJECTION_PATTERNS:
                if pattern.search(text):
                    injection_detected = True
                    # Neutralize indirect prompt injection text segment
                    clean_text = pattern.sub("[REDACTED_INDIRECT_PROMPT_INJECTION]", clean_text)

            sanitized_chunk = chunk.model_copy()
            sanitized_chunk.text = clean_text
            sanitized_list.append((sanitized_chunk, score))

        return sanitized_list, injection_detected


context_filter = ContextFilter()
