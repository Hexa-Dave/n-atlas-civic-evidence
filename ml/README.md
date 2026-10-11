# Machine learning and N-ATLAS integration

This directory contains the reproducible model integration, fine-tuning, inference, and evaluation workflow. It is separated from the web application so model quality can be tested independently.

## Intended contents

- `configs/` — versioned model, training, and evaluation configuration.
- `schemas/` — model input/output schemas.
- `prompts/` — versioned task instructions where prompting is part of the pipeline.
- `src/` — N-ATLAS client, inference wrapper, preprocessing, postprocessing, validation, and model registry.
- `training/` — fine-tuning data preparation and training scripts.
- `evaluation/` — base-versus-fine-tuned benchmark runners and report generation.
- `tests/` — tests for data processing, schemas, and model adapters.

## Required evidence

Document the exact N-ATLAS model identifier and version, access method, inference settings, training method, checkpoint/adapter identifiers, dataset versions, and software versions. A generic model wrapper is not proof of actual N-ATLAS integration.

## Evaluation rules

- Maintain a human-verified held-out test set separate from training and tuning.
- Run base and fine-tuned models on the same examples under documented settings.
- Preserve raw predictions, errors, model versions, and configuration with each run.
- Report task-appropriate metrics and safety failures, including unsupported claims and lost source attribution.

Model outputs are decision support only. Human review is required before extracted claims are finalized.
