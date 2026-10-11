# Audit trail. Records material actions without copying sensitive content.
from __future__ import annotations

import json
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from civic_evidence.models.audit_event import AuditEvent
from civic_evidence.security.redaction import redact


class AuditService:
    def __init__(self, db: Session | None = None):
        self.db = db

    @staticmethod
    def _sanitize(value):
        if value is None:
            return None
        if isinstance(value, (str, int, float, bool)):
            return redact(str(value))
        if isinstance(value, dict):
            return {str(key): AuditService._sanitize(val) for key, val in value.items()}
        if isinstance(value, list):
            return [AuditService._sanitize(item) for item in value]
        return redact(str(value))

    def record(self, actor_id: str, action: str, resource_type: str, resource_id: str, detail=None):
        if not actor_id:
            raise ValueError("actor_id is required")

        payload = {"action": action, "resource_type": resource_type, "resource_id": resource_id}
        if detail is not None:
            payload["detail"] = self._sanitize(detail)

        event = {
            "id": uuid4().hex,
            "actor_id": actor_id,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "detail": json.dumps(payload, sort_keys=True),
            "created_at": datetime.now(timezone.utc),
        }

        if self.db is not None:
            row = AuditEvent(
                id=event["id"],
                actor_id=event["actor_id"],
                action=event["action"],
                resource_type=event["resource_type"],
                resource_id=event["resource_id"],
                detail=event["detail"],
            )
            self.db.add(row)
            self.db.commit()
            self.db.refresh(row)
            return {
                "id": row.id,
                "actor_id": row.actor_id,
                "action": row.action,
                "resource_type": row.resource_type,
                "resource_id": row.resource_id,
                "detail": row.detail,
                "created_at": row.created_at,
            }

        return event
