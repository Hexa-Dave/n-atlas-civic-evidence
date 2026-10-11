# Turns a benchmark run into a human-readable evaluation report.
from pathlib import Path

import json


def write_report(run: dict, output_dir: str = "artifacts/evaluation-reports") -> Path:
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{run.get('name', 'run')}.json"
    target.write_text(json.dumps(run, indent=2), encoding="utf-8")
    return target
