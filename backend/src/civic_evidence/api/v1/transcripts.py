from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/v1/cases/{case_id}/transcripts", tags=["transcripts"])


@router.post("", status_code=status.HTTP_201_CREATED)
def start_transcription(case_id: str, audio_asset_id: str) -> dict[str, str]:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/{transcript_id}")
def get_transcript(case_id: str, transcript_id: str) -> dict[str, str]:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transcript not found")
