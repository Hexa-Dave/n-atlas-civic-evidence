from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from civic_evidence.dependencies import CurrentUser, DbDep
from civic_evidence.security.authorization import require_case_access
from civic_evidence.services.audio_service import _AUDIO_STORE
from civic_evidence.services.transcription_service import TranscriptionService

_TRANSCRIPT_STORE: dict[str, dict] = {}

router = APIRouter(prefix="/v1/cases/{case_id}/transcripts", tags=["transcripts"])


@router.post("", status_code=status.HTTP_201_CREATED)
def start_transcription(
    case_id: str,
    audio_asset_id: str,
    db: DbDep = None,
    actor: CurrentUser = None,
) -> dict[str, str]:
    if actor is not None:
        require_case_access(actor, case_id)

    if audio_asset_id not in _AUDIO_STORE and db is not None:
        from civic_evidence.models.audio_asset import AudioAsset

        asset = db.get(AudioAsset, audio_asset_id)
        if asset is None or asset.case_id != case_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audio asset not found")

    actor_id = actor["sub"] if actor is not None else "system"
    try:
        transcript = TranscriptionService(db=db).transcribe(case_id, audio_asset_id, actor_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    _TRANSCRIPT_STORE[transcript["id"]] = transcript
    return transcript


@router.get("/{transcript_id}")
def get_transcript(case_id: str, transcript_id: str, actor: CurrentUser) -> dict[str, str]:
    require_case_access(actor, case_id)
    transcript = _TRANSCRIPT_STORE.get(transcript_id)
    if not transcript or transcript.get("case_id") != case_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transcript not found")
    return transcript
