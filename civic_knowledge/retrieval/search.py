# Retrieves relevant official-source passages for a question.
from pathlib import Path


def search(question: str, index_dir: str = "data/processed/civic_index", top_k: int = 5) -> list[dict]:
    if not Path(index_dir).exists():
        raise RuntimeError("Civic index not built; run index_documents.py first.")
    raise NotImplementedError("Return passages with source title and section for citation.")
