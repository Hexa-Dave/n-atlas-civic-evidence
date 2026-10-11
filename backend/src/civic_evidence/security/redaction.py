# Redaction helpers for logs and exported documents.
import re

_PATTERNS = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "[email]"),
    (re.compile(r"\b\d{3}[-. ]?\d{3}[-. ]?\d{4}\b"), "[phone]"),
]


def redact(text: str) -> str:
    # Best-effort only; do not rely on this for legal de-identification.
    for pattern, replacement in _PATTERNS:
        text = pattern.sub(replacement, text)
    return text
