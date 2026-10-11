from fastapi import APIRouter, HTTPException, status

from civic_evidence.schemas.review import ReviewDecision, ReviewEventRead

router = APIRouter(prefix="/v1/claims/{claim_id}/reviews", tags=["reviews"])


@router.post("", response_model=ReviewEventRead, status_code=status.HTTP_201_CREATED)
def record_review(claim_id: str, payload: ReviewDecision) -> ReviewEventRead:
    # Only authorized reviewers may record a decision.
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("", response_model=list[ReviewEventRead])
def list_reviews(claim_id: str) -> list[ReviewEventRead]:
    return []
