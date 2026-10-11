# Token verification for the default app configuration.
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import HTTPException, status

from civic_evidence.config import get_settings


def normalize_actor_claims(claims: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(claims, dict):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Malformed token")

    subject = claims.get("sub") or claims.get("user_id") or claims.get("username") or claims.get("email")
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token does not contain a user identity",
        )

    roles = claims.get("roles")
    if isinstance(roles, str):
        roles = [roles]
    if roles is None:
        roles = []
    if not isinstance(roles, list):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Malformed roles claim")

    normalized = dict(claims)
    normalized["sub"] = str(subject)
    normalized["roles"] = [str(role) for role in roles if str(role).strip()]
    return normalized


def create_token(subject: str, roles: list[str] | None = None, *, ttl_minutes: int | None = None) -> str:
    settings = get_settings()
    payload = {
        "sub": subject,
        "roles": roles or [],
        "iat": int(datetime.now(timezone.utc).timestamp()),
    }
    if ttl_minutes is None:
        ttl_minutes = settings.jwt_default_ttl_minutes
    payload["exp"] = int((datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes)).timestamp())
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def verify_token(token: str) -> dict[str, Any]:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    settings = get_settings()
    try:
        claims = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc

    return normalize_actor_claims(claims)
