from fastapi import APIRouter, HTTPException, status

from civic_evidence.config import get_settings
from civic_evidence.security.authentication import create_token

router = APIRouter(prefix="/v1", tags=["auth"])


@router.post("/auth/token")
def create_demo_auth_token() -> dict[str, object]:
    settings = get_settings()
    if not settings.allow_demo_auth or settings.app_env not in {"development", "test"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Demo auth is disabled in this environment",
        )

    token = create_token(settings.demo_user_id, list(settings.demo_roles))
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": settings.demo_user_id,
        "roles": list(settings.demo_roles),
    }
