# Speech-to-text orchestration.
from __future__ import annotations

import json
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from civic_evidence.audit.audit_service import AuditService
from civic_evidence.models.audio_asset import AudioAsset
from civic_evidence.models.case import Case
from civic_evidence.models.model_run import ModelRun
from civic_evidence.models.transcript import Transcript


class TranscriptionService:
    def __init__(self, db: Session | None = None):
        self.db = db

    def transcribe(self, case_id: str, audio_asset_id: str, actor_id: str):
        if self.db is not None:
            case = self.db.get(Case, case_id)
            asset = self.db.get(AudioAsset, audio_asset_id)
            if case is None:
                raise KeyError(f"Case '{case_id}' not found")
            if asset is None or asset.case_id != case_id:
                raise KeyError(f"Audio asset '{audio_asset_id}' not found")
        else:
            from civic_evidence.services.audio_service import _AUDIO_STORE
            from civic_evidence.services.case_service import CaseService

            try:
                CaseService().get_case(case_id, actor_id)
            except KeyError as exc:
                raise KeyError(f"Case '{case_id}' not found") from exc
            if audio_asset_id not in _AUDIO_STORE or _AUDIO_STORE[audio_asset_id].get("case_id") != case_id:
                raise KeyError(f"Audio asset '{audio_asset_id}' not found")

        model_run_id = uuid4().hex
        started_at = datetime.now(timezone.utc)
        model_run = {
            "id": model_run_id,
            "task": "transcription",
            "model_id": "local-demo",
            "model_version": "offline",
            "config_json": json.dumps({"provider": "demo-offline", "mode": "safe-fallback"}),
            "started_at": started_at,
            "finished_at": datetime.now(timezone.utc),
        }

        transcript_id = uuid4().hex
        transcript = {
            "id": transcript_id,
            "case_id": case_id,
            "audio_asset_id": audio_asset_id,
            "language": "en-US",
            "status": "completed",
            "text": "Sample transcript: the witness described a delay and a document requirement. This transcription is produced by a safe local fallback when no speech-to-text provider is configured.",
            "created_at": datetime.now(timezone.utc),
        }

        if self.db is not None:
            model_row = ModelRun(
                id=model_run["id"],
                task=model_run["task"],
                model_id=model_run["model_id"],
                model_version=model_run["model_version"],
                config_json=model_run["config_json"],
                started_at=model_run["started_at"],
                finished_at=model_run["finished_at"],
            )
            self.db.add(model_row)
            transcript_row = Transcript(
                id=transcript["id"],
                case_id=transcript["case_id"],
                audio_asset_id=transcript["audio_asset_id"],
                language=transcript["language"],
            )
            self.db.add(transcript_row)
            self.db.commit()

        AuditService(db=self.db).record(
            actor_id=actor_id,
            action="transcription_completed",
            resource_type="transcript",
            resource_id=transcript["id"],
            detail={
                "case_id": case_id,
                "audio_asset_id": audio_asset_id,
                "model_id": "local-demo",
                "fallback": True,
            },
        )
        return transcript
