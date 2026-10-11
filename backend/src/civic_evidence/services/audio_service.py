# Audio ingestion: validation, hashing, and storage delegation.
from __future__ import annotations

import hashlib
import io
from datetime import datetime, timezone
from uuid import uuid4

from civic_evidence.config import get_settings
from civic_evidence.services.case_service import CaseService
from civic_evidence.storage.audio_storage import LocalAudioStorage

_AUDIO_STORE: dict[str, dict] = {}


class AudioService:
    def __init__(self, db=None, storage=None):
        self.db = db
        self.storage = storage or LocalAudioStorage()

    def store_upload(self, case_id: str, filename: str, content_type: str, stream, actor_id: str) -> dict:
        if not filename:
            raise ValueError("Filename is required")

        case = CaseService().get_case(case_id, actor_id)
        if not case.consent_recorded:
            raise PermissionError("Case consent must be recorded before uploading audio")

        allowed_types = {"audio/mpeg", "audio/mp3", "audio/wav", "audio/x-wav", "audio/mp4", "audio/m4a"}
        if content_type and content_type.lower() not in allowed_types:
            raise ValueError(f"Unsupported audio content type: {content_type}")

        data = stream.read()
        if not data:
            raise ValueError("Audio upload is empty")

        max_bytes = get_settings().max_upload_mb * 1024 * 1024
        if len(data) > max_bytes:
            raise ValueError("Audio upload exceeds the configured size limit")

        storage_key = f"{case_id}/{uuid4().hex}.{filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'bin'}"
        saved_path = self.storage.save(storage_key, io.BytesIO(data))
        sha256 = hashlib.sha256(data).hexdigest()

        asset = {
            "id": uuid4().hex,
            "case_id": case_id,
            "filename": filename,
            "content_type": content_type,
            "storage_key": storage_key,
            "sha256": sha256,
            "saved_path": saved_path,
            "created_at": datetime.now(timezone.utc),
            "uploaded_by": actor_id,
        }
        _AUDIO_STORE[asset["id"]] = asset
        return asset
