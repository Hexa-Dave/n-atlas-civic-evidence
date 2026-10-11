# Storage adapter for permitted audio assets.
from pathlib import Path

from civic_evidence.config import get_settings


class LocalAudioStorage:
    def __init__(self, base_dir: str | None = None):
        self.base_dir = Path(base_dir or get_settings().audio_storage_dir)

    def save(self, storage_key: str, stream) -> str:
        target = self.base_dir / storage_key
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(stream.read())
        return str(target)

    def delete(self, storage_key: str) -> None:
        target = self.base_dir / storage_key
        if target.exists():
            target.unlink()
