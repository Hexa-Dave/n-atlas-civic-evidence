from fastapi import APIRouter, HTTPException, status

from civic_evidence.schemas.report import ReportRead

router = APIRouter(prefix="/v1/cases/{case_id}/reports", tags=["reports"])


@router.post("", response_model=ReportRead, status_code=status.HTTP_201_CREATED)
def generate_report(case_id: str) -> ReportRead:
    # Requires at least one human review before a report can be finalized.
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/{report_id}", response_model=ReportRead)
def get_report(case_id: str, report_id: str) -> ReportRead:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
