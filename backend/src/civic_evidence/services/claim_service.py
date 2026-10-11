# Claim extraction and persistence via the N-ATLAS model.
from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from civic_evidence.models.claim import Claim
from ml.src.postprocessing import parse_json_objects

_CLAIM_STORE: dict[str, dict] = {}


class ClaimService:
    def __init__(self, db: Session | None = None, model_client=None):
        self.db = db
        self.model_client = model_client

    def extract_claims(self, case_id: str, transcript_id: str, actor_id: str) -> list[dict]:
        del actor_id
        if self.model_client is None:
            return []

        raw_output = self.model_client.complete(
            f"Extract claims for case_id={case_id} transcript_id={transcript_id} as JSON objects."
        )
        records = []
        for item in parse_json_objects(raw_output):
            text = str(item.get("claim_text") or item.get("text") or "").strip()
            segment_id = str(item.get("source_segment_id") or item.get("segment_id") or transcript_id)
            if not text:
                continue
            claim_id = uuid4().hex
            record = {
                "id": claim_id,
                "case_id": case_id,
                "transcript_id": transcript_id,
                "text": text,
                "status": str(item.get("status") or "unverified"),
                "source_segment_id": segment_id,
                "confidence": item.get("confidence"),
                "created_at": datetime.now(timezone.utc),
            }
            if self.db is not None:
                claim = Claim(
                    id=claim_id,
                    case_id=case_id,
                    transcript_id=transcript_id,
                    source_segment_id=segment_id,
                    text=text,
                    status=str(item.get("status") or "unverified"),
                    confidence=item.get("confidence"),
                )
                self.db.add(claim)
                self.db.commit()
                self.db.refresh(claim)
                record = {
                    "id": claim.id,
                    "case_id": claim.case_id,
                    "transcript_id": claim.transcript_id,
                    "text": claim.text,
                    "status": claim.status,
                    "source_segment_id": claim.source_segment_id,
                    "confidence": claim.confidence,
                }
            _CLAIM_STORE[claim_id] = record
            records.append(record)
        return records

    def update_claim(self, claim_id: str, patch: dict, actor_id: str) -> dict:
        del actor_id
        if self.db is not None:
            claim = self.db.get(Claim, claim_id)
            if claim is None:
                raise KeyError(f"Claim '{claim_id}' not found")
            if "text" in patch and patch["text"]:
                claim.text = str(patch["text"]).strip()
            if "status" in patch and patch["status"]:
                claim.status = str(patch["status"])
            if "confidence" in patch:
                claim.confidence = patch["confidence"]
            self.db.add(claim)
            self.db.commit()
            self.db.refresh(claim)
            return {
                "id": claim.id,
                "case_id": claim.case_id,
                "transcript_id": claim.transcript_id,
                "text": claim.text,
                "status": claim.status,
                "source_segment_id": claim.source_segment_id,
                "confidence": claim.confidence,
            }
        if claim_id not in _CLAIM_STORE:
            raise KeyError(f"Claim '{claim_id}' not found")

        record = _CLAIM_STORE[claim_id]
        if "text" in patch and patch["text"]:
            record["text"] = str(patch["text"]).strip()
        if "status" in patch and patch["status"]:
            record["status"] = str(patch["status"])
        if "confidence" in patch:
            record["confidence"] = patch["confidence"]
        return record
