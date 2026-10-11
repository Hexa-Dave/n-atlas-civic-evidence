from fastapi import APIRouter, HTTPException, UploadFile, status

router = APIRouter(prefix="/v1/cases/{case_id}/audio", tags=["audio"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def upload_audio(case_id: str, file: UploadFile) -> dict[str, str]:
    # Enforce size, content-type, consent, and authorization before storing.
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("")
def list_audio(case_id: str) -> list[dict[str, str]]:
    return []
