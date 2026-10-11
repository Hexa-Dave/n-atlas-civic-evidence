from fastapi import APIRouter, HTTPException, status

from civic_evidence.schemas.claim import ClaimRead, ClaimUpdate

router = APIRouter(prefix="/v1/cases/{case_id}/claims", tags=["claims"])


@router.post("/extract")
def extract_claims(case_id: str, transcript_id: str) -> list[ClaimRead]:
    # Extraction runs through the N-ATLAS model; results stay unverified.
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("", response_model=list[ClaimRead])
def list_claims(case_id: str) -> list[ClaimRead]:
    return []


@router.patch("/{claim_id}", response_model=ClaimRead)
def update_claim(case_id: str, claim_id: str, payload: ClaimUpdate) -> ClaimRead:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
