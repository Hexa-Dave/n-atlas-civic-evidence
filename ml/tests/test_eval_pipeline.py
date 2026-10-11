import json
from pathlib import Path

from civic_knowledge.ingestion.extract_passages import extract_passages
from civic_knowledge.ingestion.ingest_documents import ingest_sources
from ml.evaluation.metrics import compute_metrics
from ml.evaluation.run_benchmark import main


def test_metric_matching_tracks_precision_recall_and_source_attribution():
    gold = [
        {"claim_id": "c1", "text": "A resident must register before the deadline.", "source_segment_id": "s1"},
        {"claim_id": "c2", "text": "The form must be submitted in person.", "source_segment_id": "s2"},
    ]
    predicted = [
        {"claim_id": "c1", "text": "A resident must register before the deadline.", "source_segment_id": "s1"},
        {"claim_id": "c3", "text": "The form is filed online.", "source_segment_id": "s3"},
    ]

    metrics = compute_metrics(gold, predicted)
    assert metrics["tp"] == 1
    assert metrics["fp"] == 1
    assert metrics["fn"] == 1
    assert metrics["precision"] == 0.5
    assert metrics["recall"] == 0.5
    assert metrics["source_attribution"] == 0.5


def test_extract_passages_and_ingestion_create_processed_records(tmp_path):
    document = {
        "source_id": "example-elections-authority",
        "source_title": "Example Elections Authority",
        "title": "Voter registration procedure",
        "section": "Registration requirements",
        "text": "Eligible voters must register before the deadline. They must provide identification.",
        "url": "https://example.gov/voter-registration",
        "jurisdiction": "US-XX",
    }

    passages = extract_passages(document)
    assert len(passages) == 2
    assert passages[0]["passage_id"].startswith("example-elections-authority")

    output_dir = tmp_path / "processed"
    ingest_sources(output_dir=str(output_dir))
    run_file = output_dir / "example-elections-authority.json"
    assert run_file.exists()
    payload = json.loads(run_file.read_text(encoding="utf-8"))
    assert payload["source_id"] == "example-elections-authority"


def test_run_benchmark_reports_empty_manifest_without_crashing(tmp_path):
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"name": "demo", "samples": []}), encoding="utf-8")
    out = tmp_path / "report.json"

    report = main(manifest_path=str(manifest), output_path=str(out))
    assert report["status"] == "no_data"
    assert out.exists()
