from fastapi import APIRouter, HTTPException, UploadFile, status

from civic_evidence.services.audio_service import AudioService, _AUDIO_STORE

router = APIRouter(prefix="/v1/cases/{case_id}/audio", tags=["audio"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def upload_audio(case_id: str, file: UploadFile) -> dict[str, str]:
    try:
        asset = AudioService().store_upload(
            case_id=case_id,
            filename=file.filename or "upload.bin",
            content_type=file.content_type or "application/octet-stream",
            stream=file.file,
            actor_id="system",
        )
    except (KeyError, PermissionError, ValueError) as exc:
        detail = str(exc)
        status_code = status.HTTP_404_NOT_FOUND if isinstance(exc, KeyError) else status.HTTP_400_BAD_REQUEST
        if isinstance(exc, PermissionError):
            status_code = status.HTTP_403_FORBIDDEN
        raise HTTPException(status_code=status_code, detail=detail) from exc

    return {
        "id": asset["id"],
        "case_id": asset["case_id"],
        "filename": asset["filename"],
        "content_type": asset["content_type"],
        "storage_key": asset["storage_key"],
        "sha256": asset["sha256"],
    }


@router.get("")
def list_audio(case_id: str) -> list[dict[str, str]]:
    return [
        {
            "id": asset["id"],
            "case_id": asset["case_id"],
            "filename": asset["filename"],
            "content_type": asset["content_type"],
            "storage_key": asset["storage_key"],
        }
        for asset in _AUDIO_STORE.values()
        if asset.get("case_id") == case_id
    ]
