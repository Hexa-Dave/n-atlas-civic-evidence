# Storage adapter for generated documents (transcripts, reports).
from pathlib import Path

from civic_evidence.config import get_settings


class LocalDocumentStorage:
    def __init__(self, base_dir: str | None = None):
        self.base_dir = Path(base_dir or get_settings().document_storage_dir)

    def write_text(self, storage_key: str, content: str) -> str:
        target = self.base_dir / storage_key
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return str(target)
