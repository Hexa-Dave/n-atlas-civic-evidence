# Token verification. Replace the stub with a real identity provider integration.
from fastapi import HTTPException, status


def verify_token(token: str) -> dict:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    raise NotImplementedError("Verify the token signature and return the claims.")
