from fastapi import APIRouter, HTTPException, status

from civic_evidence.dependencies import CurrentUser, DbDep
from civic_evidence.schemas.report import ReportRead
from civic_evidence.security.authorization import require_case_access, require_reviewer
from civic_evidence.services.report_service import ReportService

router = APIRouter(prefix="/v1/cases/{case_id}/reports", tags=["reports"])


@router.post("", response_model=ReportRead, status_code=status.HTTP_201_CREATED)
def generate_report(case_id: str, db: DbDep, actor: CurrentUser) -> ReportRead:
    require_case_access(actor, case_id)
    require_reviewer(actor)
    try:
        return ReportService(db=db).generate(case_id=case_id, actor_id=actor["sub"])
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{report_id}", response_model=ReportRead)
def get_report(case_id: str, report_id: str, actor: CurrentUser) -> ReportRead:
    require_case_access(actor, case_id)
    from civic_evidence.services.report_service import _REPORT_STORE

    if report_id not in _REPORT_STORE:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    return ReportRead.model_validate(_REPORT_STORE[report_id])
