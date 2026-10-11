# Fetches and normalizes registered sources into the processed store.
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import yaml

from civic_knowledge.ingestion.extract_passages import extract_passages

REGISTRY = Path("civic_knowledge/sources/source_registry.yaml")


def load_registry() -> list[dict]:
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8")) or {}
    return list(data.get("sources", []))


def ingest_sources(registry_path: str = str(REGISTRY), output_dir: str = "data/processed/civic_sources") -> list[dict]:
    registry = Path(registry_path)
    documents = []
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for source in load_registry() if str(registry) == str(REGISTRY) else yaml.safe_load(registry.read_text(encoding="utf-8")).get("sources", []):
        record = {
            "source_id": source.get("id"),
            "source_title": source.get("title"),
            "title": source.get("title"),
            "section": "Overview",
            "content": source.get("notes") or source.get("title") or "",
            "url": source.get("url"),
            "jurisdiction": source.get("jurisdiction"),
            "published": source.get("published"),
            "accessed": source.get("accessed") or date.today().isoformat(),
            "status": source.get("status", "unverified"),
            "publisher": source.get("publisher"),
        }
        passages = extract_passages(record)
        record["passages"] = passages
        documents.append(record)
        target = output_path / f"{record['source_id']}.json"
        target.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")

    return documents


def main() -> None:
    ingest_sources()


if __name__ == "__main__":
    main()
