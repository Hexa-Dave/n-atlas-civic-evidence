from fastapi import APIRouter, HTTPException, status

from civic_evidence.dependencies import CurrentUser, DbDep
from civic_evidence.schemas.case import CaseCreate, CaseRead
from civic_evidence.security.authorization import require_case_access
from civic_evidence.services.case_service import CaseService

router = APIRouter(prefix="/v1/cases", tags=["cases"])


@router.get("", response_model=list[CaseRead])
def list_cases(db: DbDep, actor: CurrentUser) -> list[CaseRead]:
    del actor
    return CaseService(db=db).list_cases(actor_id="system")


@router.post("", response_model=CaseRead, status_code=status.HTTP_201_CREATED)
def create_case(payload: CaseCreate, db: DbDep, actor: CurrentUser) -> CaseRead:
    return CaseService(db=db).create_case(payload=payload, actor_id=actor["sub"])


@router.get("/{case_id}", response_model=CaseRead)
def get_case(case_id: str, db: DbDep, actor: CurrentUser) -> CaseRead:
    require_case_access(actor, case_id)
    try:
        return CaseService(db=db).get_case(case_id=case_id, actor_id=actor["sub"])
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found") from exc


@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_case(case_id: str, actor: CurrentUser) -> None:
    require_case_access(actor, case_id)
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
