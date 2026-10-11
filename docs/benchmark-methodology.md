# Benchmark methodology

## Test set

- Held-out and human-verified; never used for training or tuning.
- Stored under `data/benchmark/` with a manifest recording provenance.
- Prefer synthetic or redacted examples; do not commit private data.

## Procedure

1. Freeze the test set version (hash the manifest).
2. Run base and fine-tuned models on identical examples and settings.
3. Preserve raw predictions, configuration, and model versions per run.
4. Score with task-appropriate metrics.

## Metrics

- Claim extraction: precision, recall, and F1 by claim type.
- Source attribution: share of claims with a valid `source_segment_id`.
- Safety: unsupported-claim rate and unsupported-citation rate.
- Incident classification: per-class precision and recall.

## Reporting

Distinguish measured results from targets. Report confidence intervals or sample
sizes, and list known failure modes. Outputs belong in `artifacts/evaluation-reports/`.
