import os
from typing import Tuple, Dict, Any


class FileValidator:
    """Validates document files and performs security/malware safety checks."""

    ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp"}
    MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024  # 15 MB limit

    SUSPICIOUS_SIGNATURES = [
        b"%PDF-",  # Valid PDF header
        b"\x89PNG",  # PNG header
        b"\xff\xd8\xff",  # JPEG header
    ]

    MALICIOUS_PATTERNS = [
        b"/JavaScript",
        b"/JS",
        b"/Launch",
        b"/EmbeddedFile",
        b"<script>",
        b"eval(",
    ]

    def validate(self, file_bytes: bytes, file_name: str) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Executes File Validation and Malware Security checks.
        Returns:
            Tuple[is_valid, error_reason, metadata]
        """
        # 1. File size check
        if len(file_bytes) == 0:
            return False, "File is empty (0 bytes).", {}

        if len(file_bytes) > self.MAX_FILE_SIZE_BYTES:
            return False, f"File size exceeds maximum limit of {self.MAX_FILE_SIZE_BYTES // (1024*1024)}MB.", {}

        # 2. Extension check
        _, ext = os.path.splitext(file_name.lower())
        if ext not in self.ALLOWED_EXTENSIONS:
            return False, f"Unsupported file extension '{ext}'. Allowed: {list(self.ALLOWED_EXTENSIONS)}", {}

        # 3. Header signature check
        has_valid_header = any(file_bytes.startswith(sig) for sig in self.SUSPICIOUS_SIGNATURES)
        if not has_valid_header:
            return False, "File header signature does not match allowed PDF/Image formats.", {}

        # 4. Security / Malware / Script check
        for pattern in self.MALICIOUS_PATTERNS:
            if pattern in file_bytes:
                return False, f"Security Violation: File contains potentially malicious payload pattern '{pattern.decode('utf-8', errors='ignore')}'.", {}

        metadata = {
            "file_name": file_name,
            "file_size_bytes": len(file_bytes),
            "extension": ext,
            "security_passed": True,
        }
        return True, "", metadata


file_validator = FileValidator()
