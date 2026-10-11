from fastapi import APIRouter, HTTPException, status

from civic_evidence.schemas.case import CaseCreate, CaseRead

router = APIRouter(prefix="/v1/cases", tags=["cases"])


@router.get("", response_model=list[CaseRead])
def list_cases() -> list[CaseRead]:
    # TODO: delegate to case_service and enforce authorization.
    return []


@router.post("", response_model=CaseRead, status_code=status.HTTP_201_CREATED)
def create_case(payload: CaseCreate) -> CaseRead:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/{case_id}", response_model=CaseRead)
def get_case(case_id: str) -> CaseRead:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")


@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_case(case_id: str) -> None:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
