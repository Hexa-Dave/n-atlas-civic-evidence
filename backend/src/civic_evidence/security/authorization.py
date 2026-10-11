# Server-side authorization checks. Never trust client-supplied identifiers.
from fastapi import HTTPException, status


def require_case_access(actor: dict, case_id: str) -> None:
    # Confirm the actor holds an explicit grant for this case.
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized for this case")


def require_reviewer(actor: dict) -> None:
    roles = set(actor.get("roles", []))
    if not roles.intersection({"reviewer", "admin"}):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Reviewer role required")
