# Task-appropriate metrics for claim extraction and incident classification.
from __future__ import annotations

import re
from collections.abc import Iterable


def _normalize_text(value: object) -> str:
    if value is None:
        return ""
    text = str(value).lower()
    return " ".join(re.findall(r"[a-z0-9]+", text))


def _identity_keys(item: dict) -> list[str]:
    if not isinstance(item, dict):
        return []
    keys = [
        item.get("claim_id"),
        item.get("id"),
        item.get("name"),
        item.get("label"),
        item.get("text"),
        item.get("statement"),
        item.get("excerpt"),
        item.get("source_segment_id"),
        item.get("source_id"),
    ]
    return [str(value) for value in keys if value not in (None, "")]


def _match_key(item: dict) -> str:
    raw = _identity_keys(item)
    if not raw:
        return ""
    return _normalize_text(raw[0])


def prf(tp: int, fp: int, fn: int) -> dict[str, float]:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}


def _find_match(gold_item: dict, predicted: Iterable[dict]) -> dict | None:
    target_keys = {_normalize_text(key) for key in _identity_keys(gold_item) if key}
    target_text = _normalize_text(gold_item.get("text") or gold_item.get("statement") or gold_item.get("excerpt") or "")
    for candidate in predicted:
        if not isinstance(candidate, dict):
            continue
        candidate_keys = {_normalize_text(key) for key in _identity_keys(candidate) if key}
        if target_keys and candidate_keys and (target_keys & candidate_keys):
            return candidate
        if target_text and _normalize_text(candidate.get("text") or candidate.get("statement") or candidate.get("excerpt") or "") == target_text:
            return candidate
    return None


def compute_metrics(gold: list[dict], predicted: list[dict]) -> dict[str, float]:
    gold_items = list(gold or [])
    predicted_items = list(predicted or [])

    matched_gold = set()
    matched_predicted = set()
    source_attribution = 0

    for index, gold_item in enumerate(gold_items):
        match = _find_match(gold_item, [predicted_items[i] for i in range(len(predicted_items)) if i not in matched_predicted])
        if match is None:
            continue
        gold_index = gold_items.index(gold_item)
        pred_index = predicted_items.index(match)
        matched_gold.add(gold_index)
        matched_predicted.add(pred_index)
        if gold_item.get("source_segment_id") or gold_item.get("source_id") or gold_item.get("source_title"):
            source_attribution += 1

    tp = len(matched_gold)
    fp = len(predicted_items) - len(matched_predicted)
    fn = len(gold_items) - len(matched_gold)
    base = prf(tp, fp, fn)

    source_rate = source_attribution / len(gold_items) if gold_items else 1.0
    unsupported = 0
    for item in predicted_items:
        if item.get("unsupported") is True or item.get("is_unsupported") is True or item.get("status") == "unsupported":
            unsupported += 1
    unsupported_rate = unsupported / len(predicted_items) if predicted_items else 0.0

    return {
        **base,
        "source_attribution": source_rate,
        "unsupported_claim_rate": unsupported_rate,
        "tp": tp,
        "fp": fp,
        "fn": fn,
    }
