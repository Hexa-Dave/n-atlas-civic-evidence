# Report assembly. Testimony and civic guidance stay in separate sections.
from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from civic_evidence.models.claim import Claim
from civic_evidence.schemas.report import ReportCitation, ReportRead, ReportSection
from civic_evidence.services.claim_service import _CLAIM_STORE

_REPORT_STORE: dict[str, dict] = {}


class ReportService:
    def __init__(self, db: Session | None = None):
        self.db = db

    def generate(self, case_id: str, actor_id: str) -> ReportRead:
        del actor_id
        if self.db is not None:
            reviewed_claims = self.db.query(Claim).filter(
                Claim.case_id == case_id,
                Claim.status.in_({"accepted", "edited", "rejected", "flagged"}),
            ).all()
        else:
            reviewed_claims = [
                claim
                for claim in _CLAIM_STORE.values()
                if claim.get("case_id") == case_id and claim.get("status") in {"accepted", "edited", "rejected", "flagged"}
            ]
        if not reviewed_claims:
            raise ValueError("At least one reviewed claim is required before finalizing a report")

        if self.db is not None:
            testimony_rows = [
                {
                    "text": claim.text,
                    "status": claim.status,
                    "confidence": claim.confidence,
                    "source_segment_id": claim.source_segment_id,
                }
                for claim in reviewed_claims
            ]
        else:
            testimony_rows = reviewed_claims

        testimony_text = "\n".join(
            f"- {claim['text']} (status={claim['status']}, confidence={claim.get('confidence')})"
            for claim in testimony_rows
        )
        report = {
            "id": uuid4().hex,
            "case_id": case_id,
            "status": "finalized",
            "sections": [
                ReportSection(
                    heading="Testimony summary",
                    body=testimony_text,
                    citations=[ReportCitation(title="Source segment", source_id=claim.get("source_segment_id")) for claim in testimony_rows],
                    is_testimony=True,
                ),
                ReportSection(
                    heading="Civic guidance",
                    body="Official procedure and legal guidance should be reviewed separately from witness testimony and kept distinct in the final report.",
                    citations=[],
                    is_testimony=False,
                ),
            ],
            "generated_at": datetime.now(timezone.utc),
        }
        _REPORT_STORE[report["id"]] = report
        return ReportRead.model_validate(report)
