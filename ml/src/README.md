# ML source modules

This directory contains reusable model integration and inference code.

Expected modules include:
- `atlas_client.py` — the actual N-ATLAS access adapter.
- `inference.py` — task execution and model invocation.
- `preprocessing.py` — input normalization that preserves source identifiers.
- `postprocessing.py` — output normalization.
- `validation.py` — schema and consistency checks.
- `model_registry.py` — explicit model/version/configuration references.

Keep source references attached throughout processing. If the model returns invalid or incomplete data, return a controlled error or clearly flagged partial result rather than inventing missing values. Keep provider-specific code behind a small interface so the rest of the application can be tested with a fake adapter.
