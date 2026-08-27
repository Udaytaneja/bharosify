from enum import Enum


class PerceptionStatus(str, Enum):
    """Structured Status Codes for Document Perception Pipeline."""

    SUCCESS = "SUCCESS"
    MODEL_UNAVAILABLE = "MODEL_UNAVAILABLE"
    INVALID_DOCUMENT = "INVALID_DOCUMENT"
    OCR_FAILURE = "OCR_FAILURE"
    LAYOUT_FAILURE = "LAYOUT_FAILURE"
    TIMEOUT = "TIMEOUT"
    RESOURCE_ERROR = "RESOURCE_ERROR"
