# Shared FastAPI dependencies.
from typing import Annotated, Iterator

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from civic_evidence.config import Settings, get_settings

_engine = None
_SessionLocal: sessionmaker | None = None


def get_db() -> Iterator[Session]:
    global _engine, _SessionLocal
    if _SessionLocal is None:
        _engine = create_engine(get_settings().database_url, pool_pre_ping=True)
        _SessionLocal = sessionmaker(bind=_engine, autoflush=False, expire_on_commit=False)
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(authorization: Annotated[str | None, Header()] = None) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    # TODO: verify the token signature and resolve a real user identity.
    return authorization.split(" ", 1)[1]


SettingsDep = Annotated[Settings, Depends(get_settings)]
DbDep = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[str, Depends(get_current_user)]
