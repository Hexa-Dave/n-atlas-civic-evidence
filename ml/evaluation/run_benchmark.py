# Runs base and fine-tuned models on the held-out benchmark under identical settings.
from __future__ import annotations

import argparse
import json
from pathlib import Path

from ml.evaluation.metrics import compute_metrics


def _empty_report() -> dict:
    return {
        "status": "no_data",
        "samples": 0,
        "metrics": {"precision": 0.0, "recall": 0.0, "f1": 0.0, "source_attribution": 0.0, "unsupported_claim_rate": 0.0},
        "summary": {"tp": 0, "fp": 0, "fn": 0},
    }


def main(manifest_path: str = "data/benchmark/manifest.json", output_path: str = "artifacts/evaluation-reports/benchmark_report.json") -> dict:
    manifest = Path(manifest_path)
    if not manifest.exists():
        raise FileNotFoundError(f"Benchmark manifest not found: {manifest}")

    payload = json.loads(manifest.read_text(encoding="utf-8"))
    samples = payload.get("samples", [])
    if not samples:
        report = _empty_report()
    else:
        totals = {"tp": 0, "fp": 0, "fn": 0, "source_attribution": 0.0, "unsupported_claim_rate": 0.0}
        for sample in samples:
            gold = list(sample.get("gold_claims", []))
            predicted = list(sample.get("predicted_claims", gold))
            scores = compute_metrics(gold, predicted)
            totals["tp"] += scores["tp"]
            totals["fp"] += scores["fp"]
            totals["fn"] += scores["fn"]
            totals["source_attribution"] += scores["source_attribution"]
            totals["unsupported_claim_rate"] += scores["unsupported_claim_rate"]

        base = {"precision": 0.0, "recall": 0.0, "f1": 0.0}
        if totals["tp"] or totals["fp"] or totals["fn"]:
            precision = totals["tp"] / (totals["tp"] + totals["fp"]) if totals["tp"] + totals["fp"] else 0.0
            recall = totals["tp"] / (totals["tp"] + totals["fn"]) if totals["tp"] + totals["fn"] else 0.0
            f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
            base = {"precision": precision, "recall": recall, "f1": f1}
        report = {
            "status": "ok",
            "samples": len(samples),
            "metrics": {
                **base,
                "source_attribution": totals["source_attribution"] / len(samples) if samples else 0.0,
                "unsupported_claim_rate": totals["unsupported_claim_rate"] / len(samples) if samples else 0.0,
            },
            "summary": {"tp": totals["tp"], "fp": totals["fp"], "fn": totals["fn"]},
        }

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the civic benchmark manifest and save metrics.")
    parser.add_argument("--manifest", default="data/benchmark/manifest.json", help="Path to the benchmark manifest JSON.")
    parser.add_argument("--output", default="artifacts/evaluation-reports/benchmark_report.json", help="Where to write the benchmark report.")
    args = parser.parse_args()
    main(manifest_path=args.manifest, output_path=args.output)
