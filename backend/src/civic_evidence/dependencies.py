# Shared FastAPI dependencies.
from typing import Annotated, Iterator

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from civic_evidence.config import Settings, get_settings
from civic_evidence.models.audit_event import AuditEvent
from civic_evidence.models.audio_asset import AudioAsset
from civic_evidence.models.case import Base, Case
from civic_evidence.models.claim import Claim
from civic_evidence.models.model_run import ModelRun
from civic_evidence.models.review_event import ReviewEvent
from civic_evidence.models.transcript import Transcript
from civic_evidence.security.authentication import verify_token

# Import model modules to ensure SQLAlchemy metadata is populated before create_all().
for _model in (Case, Claim, ReviewEvent, AudioAsset, Transcript, ModelRun, AuditEvent):
    pass

_engine = None
_SessionLocal: sessionmaker | None = None


def initialize_database() -> None:
    global _engine, _SessionLocal
    if _SessionLocal is None:
        _engine = create_engine(get_settings().database_url, pool_pre_ping=True)
        _SessionLocal = sessionmaker(bind=_engine, autoflush=False, expire_on_commit=False)
    Base.metadata.create_all(bind=_engine)


def get_db() -> Iterator[Session]:
    initialize_database()
    assert _SessionLocal is not None
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(authorization: Annotated[str | None, Header()] = None) -> dict:
    settings = get_settings()
    if not authorization or not authorization.lower().startswith("bearer "):
        if settings.app_env == "development" and settings.allow_demo_auth:
            return {
                "sub": settings.demo_user_id,
                "roles": list(settings.demo_roles),
                "case_access": [],
            }
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    token = authorization.split(" ", 1)[1]
    claims = verify_token(token)
    subject = claims.get("sub")
    roles = list(claims.get("roles", []))
    return {
        "sub": str(subject),
        "roles": roles,
        "case_access": claims.get("case_access", []),
    }


SettingsDep = Annotated[Settings, Depends(get_settings)]
DbDep = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[dict, Depends(get_current_user)]
