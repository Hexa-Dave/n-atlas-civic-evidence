from pathlib import Path

from fastapi import APIRouter, HTTPException, status

from civic_evidence.config import get_settings
from civic_knowledge.retrieval.search import search

router = APIRouter(prefix="/v1/civic-guidance", tags=["civic-guidance"])


@router.get("/search")
def search_guidance(q: str, jurisdiction: str | None = None) -> list[dict[str, str]]:
    if not q or not q.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Query is required")

    settings = get_settings()
    index_dir = str(Path(settings.civic_index_dir).resolve())
    try:
        results = search(q, index_dir=index_dir, top_k=5)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    if jurisdiction:
        results = [item for item in results if (item.get("jurisdiction") or "").lower() == jurisdiction.lower()]

    return [
        {
            "source_id": item.get("source_id", ""),
            "source_title": item.get("source_title", ""),
            "title": item.get("title", ""),
            "section": item.get("section", "Overview"),
            "excerpt": item.get("excerpt", ""),
            "url": item.get("url", ""),
            "jurisdiction": item.get("jurisdiction", ""),
        }
        for item in results
    ]
