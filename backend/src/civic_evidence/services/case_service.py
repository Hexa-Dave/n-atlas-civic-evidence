# Case lifecycle operations.
from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from civic_evidence.models.case import Case
from civic_evidence.schemas.case import CaseCreate, CaseRead

_CASE_STORE: dict[str, dict] = {}


class CaseService:
    def __init__(self, db: Session | None = None):
        self.db = db

    def create_case(self, payload: CaseCreate, actor_id: str) -> CaseRead:
        del actor_id
        if self.db is not None:
            case = Case(
                id=uuid4().hex,
                title=payload.title,
                description=payload.description,
                consent_recorded=payload.consent_recorded,
                status="draft",
            )
            self.db.add(case)
            self.db.commit()
            self.db.refresh(case)
            return CaseRead.model_validate(
                {
                    "id": case.id,
                    "title": case.title,
                    "description": case.description,
                    "consent_recorded": case.consent_recorded,
                    "status": case.status,
                    "created_at": case.created_at,
                }
            )

        case_id = uuid4().hex
        case_data = {
            "id": case_id,
            "title": payload.title,
            "description": payload.description,
            "consent_recorded": payload.consent_recorded,
            "status": "draft",
            "created_at": datetime.now(timezone.utc),
        }
        _CASE_STORE[case_id] = case_data
        return CaseRead.model_validate(case_data)

    def list_cases(self, actor_id: str) -> list[CaseRead]:
        del actor_id
        if self.db is not None:
            rows = self.db.query(Case).order_by(Case.created_at.desc()).all()
            return [
                CaseRead.model_validate(
                    {
                        "id": row.id,
                        "title": row.title,
                        "description": row.description,
                        "consent_recorded": row.consent_recorded,
                        "status": row.status,
                        "created_at": row.created_at,
                    }
                )
                for row in rows
            ]
        return [CaseRead.model_validate(case_data) for case_data in _CASE_STORE.values()]

    def get_case(self, case_id: str, actor_id: str) -> CaseRead:
        del actor_id
        if self.db is not None:
            row = self.db.get(Case, case_id)
            if row is None:
                raise KeyError(f"Case '{case_id}' not found")
            return CaseRead.model_validate(
                {
                    "id": row.id,
                    "title": row.title,
                    "description": row.description,
                    "consent_recorded": row.consent_recorded,
                    "status": row.status,
                    "created_at": row.created_at,
                }
            )
        if case_id not in _CASE_STORE:
            raise KeyError(f"Case '{case_id}' not found")
        return CaseRead.model_validate(_CASE_STORE[case_id])
