# Incident-report pipeline: text report -> claims/classification -> review -> report.
from __future__ import annotations

import re
from uuid import uuid4

from civic_evidence.dependencies import initialize_database
from civic_evidence.models.claim import Claim
from civic_evidence.schemas.case import CaseCreate
from civic_evidence.services.case_service import CaseService
from civic_evidence.services.claim_service import ClaimService
from civic_evidence.services.report_service import ReportService
from civic_evidence.services.review_service import ReviewService


def _classify_incident(report_text: str) -> str:
    lowered = report_text.lower()
    if any(token in lowered for token in ("injury", "danger", "unsafe", "assault", "violence")):
        return "safety_incident"
    if any(token in lowered for token in ("delay", "missing", "denied", "refused")):
        return "service_access_issue"
    return "general_incident"


def _split_sentences(text: str) -> list[str]:
    chunks = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    return [chunk.strip() for chunk in chunks if chunk.strip()]


async def run_incident_pipeline(case_id: str, report_text: str, actor_id: str) -> dict:
    if not report_text or not report_text.strip():
        raise ValueError("report_text is required")

    initialize_database()
    from civic_evidence.dependencies import _SessionLocal

    if _SessionLocal is None:
        raise RuntimeError("Database session factory was not initialized")

    with _SessionLocal() as db:
        case_service = CaseService(db)
        try:
            case_service.get_case(case_id, actor_id)
        except KeyError:
            case_service.create_case(
                CaseCreate(
                    title=f"Incident case {case_id}",
                    description="Created by the incident pipeline.",
                    consent_recorded=True,
                ),
                actor_id=actor_id,
            )

        classification = _classify_incident(report_text)
        claims = ClaimService(db).extract_claims(case_id, "incident-report", actor_id)
        if not claims:
            for index, sentence in enumerate(_split_sentences(report_text), start=1):
                if not sentence:
                    continue
                claim = Claim(
                    id=uuid4().hex,
                    case_id=case_id,
                    transcript_id="incident-report",
                    source_segment_id=f"incident-report-{index}",
                    text=sentence,
                    status="unverified",
                    confidence=0.7,
                )
                db.add(claim)
                db.commit()
                db.refresh(claim)
                claims.append(
                    {
                        "id": claim.id,
                        "case_id": claim.case_id,
                        "transcript_id": claim.transcript_id,
                        "text": claim.text,
                        "status": claim.status,
                        "source_segment_id": claim.source_segment_id,
                        "confidence": claim.confidence,
                    }
                )

        decisions = []
        for claim in claims:
            decisions.append(
                ReviewService(db).record_decision(
                    claim["id"],
                    "accepted",
                    "Auto-approved by the incident pipeline demo review step.",
                    actor_id,
                )
            )

        report = ReportService(db).generate(case_id, actor_id)
        return {
            "case_id": case_id,
            "classification": classification,
            "report_text": report_text,
            "claims": claims,
            "decisions": decisions,
            "report": report.model_dump(mode="json"),
        }
