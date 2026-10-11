# Fetches and normalizes registered sources into the processed store.
from pathlib import Path

import yaml

REGISTRY = Path("civic_knowledge/sources/source_registry.yaml")


def load_registry() -> list[dict]:
    return yaml.safe_load(REGISTRY.read_text(encoding="utf-8")).get("sources", [])


def main() -> None:
    raise NotImplementedError("Fetch each source, record access date, and store normalized text.")


if __name__ == "__main__":
    main()
