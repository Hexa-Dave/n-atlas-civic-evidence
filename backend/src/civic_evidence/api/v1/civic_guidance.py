from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/v1/civic-guidance", tags=["civic-guidance"])


@router.get("/search")
def search_guidance(q: str, jurisdiction: str | None = None) -> list[dict[str, str]]:
    # Returns official-source excerpts only; never mixes in witness testimony.
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
