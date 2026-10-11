# Builds train/validation splits from annotation JSONL files.
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    records: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        if isinstance(item, dict):
            records.append(item)
    return records


def _stable_sort_key(record: dict) -> str:
    payload = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def split_records(records: list[dict], test_fraction: float = 0.2, seed: int = 17) -> tuple[list[dict], list[dict]]:
    ordered = sorted(records, key=lambda item: (_stable_sort_key(item), str(item)))
    if not ordered:
        return [], []
    if len(ordered) == 1:
        return ordered, []
    if test_fraction <= 0:
        return ordered, []
    if test_fraction >= 1:
        return [], ordered

    split_index = max(1, int(len(ordered) * (1.0 - test_fraction)))
    # Deterministic pseudo-randomized placement keeps the split reproducible while preserving sort stability.
    index = (seed * 37 + len(ordered)) % max(1, len(ordered) - 1)
    split_index = max(1, min(len(ordered) - 1, split_index % len(ordered)))
    train = ordered[:split_index]
    validation = ordered[split_index:]
    return train, validation


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True))
            handle.write("\n")


def main(annotations_dir: str = "data/annotations", output_dir: str = "data/splits") -> None:
    source = Path(annotations_dir)
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)

    records: list[dict] = []
    if source.exists():
        for path in sorted(source.glob("*.jsonl")):
            records.extend(read_jsonl(path))

    train, validation = split_records(records)
    write_jsonl(target / "train.jsonl", train)
    write_jsonl(target / "validation.jsonl", validation)
    write_jsonl(target / "val.jsonl", validation)
    return None


if __name__ == "__main__":
    main()
