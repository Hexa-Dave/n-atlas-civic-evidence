# Builds train/validation splits from annotation JSONL files.
import json
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main(annotations_dir: str = "data/annotations", output_dir: str = "data/splits") -> None:
    raise NotImplementedError("Implement deterministic, seeded train/validation splitting.")


if __name__ == "__main__":
    main()
