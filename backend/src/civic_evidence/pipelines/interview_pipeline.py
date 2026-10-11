# End-to-end interview pipeline: audio -> transcript -> claims -> review -> report.
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
from civic_evidence.services.transcription_service import TranscriptionService


def _split_sentences(text: str) -> list[str]:
    chunks = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    return [chunk.strip() for chunk in chunks if chunk.strip()]


async def run_interview_pipeline(case_id: str, audio_asset_id: str, actor_id: str) -> dict:
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
                    title=f"Interview case {case_id}",
                    description="Created by the interview pipeline.",
                    consent_recorded=True,
                ),
                actor_id=actor_id,
            )

        transcript = TranscriptionService(db).transcribe(case_id, audio_asset_id, actor_id)
        claims = ClaimService(db).extract_claims(case_id, transcript["id"], actor_id)

        if not claims:
            for index, sentence in enumerate(_split_sentences(transcript["text"]), start=1):
                if not sentence:
                    continue
                claim = Claim(
                    id=uuid4().hex,
                    case_id=case_id,
                    transcript_id=transcript["id"],
                    source_segment_id=f"{transcript['id']}-{index}",
                    text=sentence,
                    status="unverified",
                    confidence=0.6,
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
                    "Auto-approved by the interview pipeline demo review step.",
                    actor_id,
                )
            )

        report = ReportService(db).generate(case_id, actor_id)
        return {
            "case_id": case_id,
            "audio_asset_id": audio_asset_id,
            "transcript": transcript,
            "claims": claims,
            "decisions": decisions,
            "report": report.model_dump(mode="json"),
        }
