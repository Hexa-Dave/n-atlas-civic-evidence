# Retrieves relevant official-source passages for a question.
from __future__ import annotations

import json
from pathlib import Path


def _tokenize(value: str) -> set[str]:
    return {token for token in value.lower().replace("-", " ").split() if token}


def search(question: str, index_dir: str = "data/processed/civic_index", top_k: int = 5) -> list[dict]:
    path = Path(index_dir)
    if not path.exists():
        raise RuntimeError("Civic index not built; run index_documents.py first.")

    index_path = path / "index.json"
    if not index_path.exists():
        raise RuntimeError("Civic index file missing; run index_documents.py first.")

    payload = json.loads(index_path.read_text(encoding="utf-8"))
    passages = payload.get("passages", [])
    if not passages:
        return []

    question_tokens = _tokenize(question)
    ranked = []
    for passage in passages:
        text = " ".join(
            part for part in [passage.get("title"), passage.get("section"), passage.get("excerpt"), passage.get("text")] if part
        )
        score = len(_tokenize(text) & question_tokens)
        if not question_tokens:
            score = 1
        ranked.append({
            "source_id": passage.get("source_id"),
            "source_title": passage.get("source_title") or passage.get("title"),
            "title": passage.get("title") or passage.get("source_title"),
            "section": passage.get("section") or "Overview",
            "excerpt": passage.get("excerpt") or passage.get("text") or "",
            "url": passage.get("url"),
            "jurisdiction": passage.get("jurisdiction"),
            "score": score,
        })

    ranked.sort(key=lambda item: (-item["score"], item["source_title"] or ""))
    return ranked[: max(1, top_k)]
