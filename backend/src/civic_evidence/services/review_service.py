# Human review workflow.
from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from civic_evidence.models.claim import Claim
from civic_evidence.models.review_event import ReviewEvent
from civic_evidence.services.claim_service import _CLAIM_STORE

_REVIEW_STORE: dict[str, dict] = {}


class ReviewService:
    def __init__(self, db: Session | None = None):
        self.db = db

    def record_decision(self, claim_id: str, decision: str, note: str | None, reviewer_id: str) -> dict:
        allowed = {"accepted", "edited", "rejected", "flagged"}
        if decision not in allowed:
            raise ValueError(f"Unsupported review decision: {decision}")

        if self.db is not None:
            claim = self.db.get(Claim, claim_id)
            if claim is None:
                raise KeyError(f"Claim '{claim_id}' not found")
            review = ReviewEvent(
                id=uuid4().hex,
                claim_id=claim_id,
                reviewer_id=reviewer_id,
                decision=decision,
                note=note,
            )
            self.db.add(review)
            claim.status = decision
            self.db.commit()
            self.db.refresh(review)
            return {
                "id": review.id,
                "claim_id": review.claim_id,
                "reviewer_id": review.reviewer_id,
                "decision": review.decision,
                "note": review.note,
                "created_at": review.created_at,
            }

        if claim_id not in _CLAIM_STORE:
            raise KeyError(f"Claim '{claim_id}' not found")

        review = {
            "id": uuid4().hex,
            "claim_id": claim_id,
            "reviewer_id": reviewer_id,
            "decision": decision,
            "note": note,
            "created_at": datetime.now(timezone.utc),
        }
        _REVIEW_STORE[review["id"]] = review
        _CLAIM_STORE[claim_id]["status"] = decision
        return review

    def reviewed_claim_ids(self, case_id: str) -> set[str]:
        return {
            claim_id
            for claim_id, claim in _CLAIM_STORE.items()
            if claim.get("case_id") == case_id and claim.get("status") in {"accepted", "edited", "rejected", "flagged"}
        }
