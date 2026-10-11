# Benchmark

This directory holds the held-out, human-verified evaluation set used to compare
base and fine-tuned models. Keep these examples out of training and tuning data.

- `manifest.json` lists the samples and their provenance.
- Record raw predictions, errors, model versions, and configuration with each run.
- Do not commit private or identifying data here; use synthetic or redacted examples.

See `docs/benchmark-methodology.md` for the evaluation protocol.
