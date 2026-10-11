# Data and benchmark assets

This directory organizes dataset metadata and approved data assets for training and evaluation.

## Intended layout

- `schemas/` — JSON Schemas and data contracts.
- `raw/` — original approved source data; normally private and excluded from Git.
- `interim/` — temporary normalized data.
- `processed/` — cleaned, redacted, versioned examples.
- `annotations/` — human labels and adjudication records.
- `splits/` — train/validation/test membership manifests.
- `benchmark/` — frozen evaluation manifest and supporting metadata.
- `manifest.json` — dataset version, provenance, license/consent status, and counts.

## Data handling rules

- Never commit private witness audio, identifying transcripts, credentials, or restricted source material.
- Include only data with documented permission, license, or other valid basis for use.
- Minimize personal data and redact identifiers when unnecessary.
- Keep test labels and examples out of training and prompt tuning.
- Record dataset versions, transformations, annotator guidance, and known limitations.
- Use synthetic data for demos and automated tests unless real data use is explicitly approved.

A valid benchmark needs defined tasks, reliable labels, documented provenance, and a reproducible evaluation procedure—not merely 500 files.
