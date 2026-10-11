from fastapi import APIRouter, HTTPException, status

from civic_evidence.dependencies import CurrentUser, DbDep
from civic_evidence.models.review_event import ReviewEvent
from civic_evidence.schemas.review import ReviewDecision, ReviewEventRead
from civic_evidence.security.authorization import require_reviewer
from civic_evidence.services.review_service import ReviewService

router = APIRouter(prefix="/v1/claims/{claim_id}/reviews", tags=["reviews"])


@router.post("", response_model=ReviewEventRead, status_code=status.HTTP_201_CREATED)
def record_review(claim_id: str, payload: ReviewDecision, db: DbDep, actor: CurrentUser) -> ReviewEventRead:
    require_reviewer(actor)
    try:
        review = ReviewService(db=db).record_decision(
            claim_id=claim_id,
            decision=payload.decision,
            note=payload.note,
            reviewer_id=actor["sub"],
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found") from exc
    return ReviewEventRead.model_validate(review)


@router.get("", response_model=list[ReviewEventRead])
def list_reviews(claim_id: str, db: DbDep, actor: CurrentUser) -> list[ReviewEventRead]:
    require_reviewer(actor)
    rows = db.query(ReviewEvent).filter(ReviewEvent.claim_id == claim_id).all()
    return [
        ReviewEventRead.model_validate(
            {
                "id": row.id,
                "claim_id": row.claim_id,
                "reviewer_id": row.reviewer_id,
                "decision": row.decision,
                "note": row.note,
                "created_at": row.created_at,
            }
        )
        for row in rows
    ]
