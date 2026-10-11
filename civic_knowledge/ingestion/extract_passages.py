# Splits normalized documents into citable passages with stable ids.
from __future__ import annotations

import re


def _split_sentences(text: str) -> list[str]:
    if not text:
        return []
    chunks = re.split(r"(?<=[.!?])\s+", text.strip())
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def extract_passages(document: dict) -> list[dict]:
    source_id = str(document.get("source_id") or document.get("id") or "unknown-source")
    source_title = document.get("source_title") or document.get("title") or "Unknown source"
    title = document.get("title") or source_title
    section = document.get("section") or "Overview"
    text = document.get("text") or document.get("excerpt") or document.get("content") or ""
    if not text:
        text = title

    segments = _split_sentences(text)
    if not segments:
        segments = [text.strip()]

    passages: list[dict] = []
    for index, segment in enumerate(segments, start=1):
        passage = {
            "source_id": source_id,
            "source_title": source_title,
            "title": title,
            "section": section,
            "passage_id": f"{source_id}:{section}:{index}",
            "excerpt": segment,
            "text": segment,
            "url": document.get("url"),
            "jurisdiction": document.get("jurisdiction"),
        }
        passages.append(passage)
    return passages
