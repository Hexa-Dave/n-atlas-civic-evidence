# Builds the retrieval index over extracted passages.
from pathlib import Path


def build_index(passages: list[dict], index_dir: str = "data/processed/civic_index") -> Path:
    target = Path(index_dir)
    target.mkdir(parents=True, exist_ok=True)
    raise NotImplementedError("Write the index and a manifest of indexed source ids.")


def main() -> None:
    raise NotImplementedError


if __name__ == "__main__":
    main()
