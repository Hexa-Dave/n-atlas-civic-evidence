# Evaluates an adapter on the held-out validation split.
from __future__ import annotations

import json
from pathlib import Path

from ml.evaluation.metrics import compute_metrics


def read_jsonl(path: str | Path) -> list[dict]:
    records: list[dict] = []
    file_path = Path(path)
    if not file_path.exists():
        return records
    for line in file_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            item = json.loads(line)
            if isinstance(item, dict):
                records.append(item)
    return records


def main(gold_path: str = "data/splits/validation.jsonl", predictions_path: str = "artifacts/predictions.jsonl") -> dict:
    gold = read_jsonl(gold_path)
    predictions = read_jsonl(predictions_path)
    return compute_metrics(gold, predictions)


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, ensure_ascii=False))
