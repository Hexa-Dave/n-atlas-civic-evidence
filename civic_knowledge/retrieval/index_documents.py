# Builds the retrieval index over extracted passages.
from __future__ import annotations

import json
from pathlib import Path


def build_index(passages: list[dict], index_dir: str = "data/processed/civic_index") -> Path:
    target = Path(index_dir)
    target.mkdir(parents=True, exist_ok=True)

    normalized = []
    source_ids = set()
    for passage in passages:
        normalized_passage = {
            "source_id": passage.get("source_id") or passage.get("id") or "unknown-source",
            "source_title": passage.get("source_title") or passage.get("title") or "Unknown source",
            "title": passage.get("title") or passage.get("source_title") or "Unknown source",
            "section": passage.get("section") or "Overview",
            "excerpt": passage.get("excerpt") or passage.get("text") or "",
            "text": passage.get("text") or passage.get("excerpt") or "",
            "url": passage.get("url"),
            "jurisdiction": passage.get("jurisdiction"),
        }
        normalized.append(normalized_passage)
        source_ids.add(normalized_passage["source_id"])

    payload = {
        "created": True,
        "source_ids": sorted(source_ids),
        "passages": normalized,
    }

    index_path = target / "index.json"
    index_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return index_path


def main() -> None:
    sample_passages = [
        {
            "source_id": "example-elections-authority",
            "source_title": "Example Elections Authority",
            "title": "Voter registration procedure",
            "section": "Registration requirements",
            "excerpt": "Eligible voters must register before the applicable deadline and provide required identification.",
            "text": "Eligible voters must register before the applicable deadline and provide required identification.",
            "url": "https://example.gov/voter-registration",
            "jurisdiction": "US-XX",
        }
    ]
    build_index(sample_passages)


if __name__ == "__main__":
    main()
