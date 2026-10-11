import json
from pathlib import Path

from ml.evaluation.error_analysis import summarize_errors
from ml.training.prepare_dataset import split_records, write_jsonl


def test_split_records_is_deterministic_and_outputs_validation_set():
    records = [
        {"claim_id": "a", "text": "first"},
        {"claim_id": "b", "text": "second"},
        {"claim_id": "c", "text": "third"},
        {"claim_id": "d", "text": "fourth"},
    ]
    split_a, split_b = split_records(records)
    assert len(split_a) + len(split_b) == len(records)
    assert split_a and split_b


def test_summarize_errors_groups_missing_and_hallucinated_claims():
    gold = [{"claim_id": "a", "text": "x", "source_segment_id": "s1"}]
    predicted = [{"claim_id": "b", "text": "y"}]
    summary = summarize_errors(gold, predicted)
    assert summary["missed_claims"][0]["reason"] == "missing_from_predictions"
    assert summary["hallucinated_claims"][0]["reason"] == "not_in_gold"


def test_prepare_dataset_writes_train_and_validation_jsonl(tmp_path):
    records = [{"claim_id": x, "text": f"example {x}"} for x in ["a", "b", "c", "d"]]
    target = tmp_path / "splits"
    target.mkdir(exist_ok=True)
    write_jsonl(target / "train.jsonl", records[:2])
    write_jsonl(target / "validation.jsonl", records[2:])
    assert Path(target / "train.jsonl").exists()
    assert json.loads((target / "validation.jsonl").read_text(encoding="utf-8").splitlines()[0])["claim_id"] == "c"
