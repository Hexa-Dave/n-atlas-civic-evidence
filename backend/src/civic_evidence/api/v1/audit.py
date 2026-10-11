from fastapi import APIRouter, HTTPException, status

from civic_evidence.audit.audit_service import AuditService
from civic_evidence.dependencies import CurrentUser, DbDep
from civic_evidence.models.audit_event import AuditEvent

router = APIRouter(prefix="/v1/audit", tags=["audit"])


@router.get("/events")
def list_events(db: DbDep, actor: CurrentUser) -> list[dict[str, object]]:
    from civic_evidence.security.authorization import require_reviewer

    require_reviewer(actor)
    rows = db.query(AuditEvent).order_by(AuditEvent.created_at.desc()).all()
    return [
        {
            "id": row.id,
            "actor_id": row.actor_id,
            "action": row.action,
            "resource_type": row.resource_type,
            "resource_id": row.resource_id,
            "detail": row.detail,
            "created_at": row.created_at,
        }
        for row in rows
    ]


@router.post("/events")
def record_event(payload: dict, db: DbDep, actor: CurrentUser) -> dict[str, object]:
    from civic_evidence.security.authorization import require_reviewer

    require_reviewer(actor)
    try:
        event = AuditService(db).record(
            actor_id=actor["sub"],
            action=str(payload.get("action") or ""),
            resource_type=str(payload.get("resource_type") or ""),
            resource_id=str(payload.get("resource_id") or ""),
            detail=payload.get("detail"),
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return event
