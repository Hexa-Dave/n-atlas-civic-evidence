# `civic_evidence` application package

This package implements the backend application. Its modules should have clear ownership and narrow interfaces.

- `main.py` — construct and configure the API application.
- `config.py` — typed configuration loaded from environment variables.
- `dependencies.py` — shared request dependencies such as database sessions and authenticated principals.
- `api/v1/` — HTTP routing and transport-level validation.
- `schemas/` — validated data-transfer objects.
- `models/` — database entities and relationships.
- `services/` — use-case logic.
- `pipelines/` — ordered processing steps for source material.
- `storage/` — storage provider interfaces and implementation.
- `security/` — access-control helpers and policy enforcement.
- `audit/` — audit event definitions and recording.

Keep model output untrusted until schema validation and application checks have succeeded. Syntactically valid output is not proof that extracted content is accurate.
