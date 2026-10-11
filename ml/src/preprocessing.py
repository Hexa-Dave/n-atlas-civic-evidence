# Normalizes transcript/report text before inference. Never rewrites meaning.


def normalize_segment(segment: dict) -> dict:
    text = " ".join(str(segment.get("text", "")).split())
    return {**segment, "text": text}


def chunk_long_text(text: str, max_chars: int = 8000) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    return [text[i : i + max_chars] for i in range(0, len(text), max_chars)]
