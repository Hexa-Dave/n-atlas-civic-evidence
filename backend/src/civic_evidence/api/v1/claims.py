from fastapi import APIRouter, HTTPException, status

from civic_evidence.dependencies import CurrentUser, DbDep
from civic_evidence.schemas.claim import ClaimRead, ClaimUpdate
from civic_evidence.security.authorization import require_case_access
from civic_evidence.services.claim_service import ClaimService

router = APIRouter(prefix="/v1/cases/{case_id}/claims", tags=["claims"])


@router.post("/extract")
def extract_claims(case_id: str, transcript_id: str, db: DbDep, actor: CurrentUser) -> list[ClaimRead]:
    require_case_access(actor, case_id)
    claims = ClaimService(db=db).extract_claims(case_id=case_id, transcript_id=transcript_id, actor_id=actor["sub"])
    return [ClaimRead.model_validate(claim) for claim in claims]


@router.get("", response_model=list[ClaimRead])
def list_claims(case_id: str, db: DbDep, actor: CurrentUser) -> list[ClaimRead]:
    require_case_access(actor, case_id)
    from civic_evidence.models.claim import Claim

    rows = db.query(Claim).filter(Claim.case_id == case_id).all()
    return [
        ClaimRead.model_validate(
            {
                "id": row.id,
                "case_id": row.case_id,
                "text": row.text,
                "status": row.status,
                "source_segment_id": row.source_segment_id,
                "confidence": row.confidence,
            }
        )
        for row in rows
    ]


@router.patch("/{claim_id}", response_model=ClaimRead)
def update_claim(case_id: str, claim_id: str, payload: ClaimUpdate, db: DbDep, actor: CurrentUser) -> ClaimRead:
    require_case_access(actor, case_id)
    try:
        updated = ClaimService(db=db).update_claim(claim_id, payload.model_dump(exclude_none=True), actor["sub"])
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found") from exc
    return ClaimRead.model_validate(updated)
