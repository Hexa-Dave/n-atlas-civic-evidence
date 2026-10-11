# Groups evaluation errors for review: missed claims, hallucinated claims,
# lost source attribution, and unsupported statements.
from __future__ import annotations


def _track_key(item: dict) -> str:
    for field in ("claim_id", "id", "claim_text", "text", "statement"):
        value = item.get(field)
        if value:
            return str(value)
    return str(item)


def summarize_errors(gold: list[dict], predicted: list[dict]) -> dict[str, list[dict]]:
    gold_by_key = {_track_key(item): item for item in gold}
    predicted_by_key = {_track_key(item): item for item in predicted}

    missed = [
        {"record": item, "reason": "missing_from_predictions"}
        for key, item in gold_by_key.items()
        if key not in predicted_by_key
    ]
    hallucinated = [
        {"record": item, "reason": "not_in_gold"}
        for key, item in predicted_by_key.items()
        if key not in gold_by_key
    ]
    missing_source = [
        {"record": item, "reason": "source_missing"}
        for item in gold
        if not item.get("source_segment_id") and not item.get("source_id")
    ]
    unsupported = [
        {"record": item, "reason": "unsupported_statement"}
        for item in predicted
        if item.get("unsupported") is True or item.get("status") == "unsupported"
    ]
    return {
        "missed_claims": missed,
        "hallucinated_claims": hallucinated,
        "missing_source_attribution": missing_source,
        "unsupported_statements": unsupported,
    }
