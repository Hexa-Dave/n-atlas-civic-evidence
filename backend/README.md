# Backend

The backend exposes the application API and coordinates persistence, authorization, file handling, model inference, civic-source retrieval, review workflows, report generation, and audit events.

## Intended contents

- `migrations/` — versioned database schema migrations.
- `src/civic_evidence/` — application package and entry point.
- `api/v1/` — versioned API route handlers.
- `schemas/` — request and response validation schemas.
- `models/` — persistence models.
- `services/` — application and domain services.
- `pipelines/` — orchestration of transcription, extraction, validation, retrieval, and report assembly.
- `storage/` — storage adapters and file metadata handling.
- `security/` — authentication, authorization, and policy enforcement.
- `audit/` — audit event handling.
- `tests/` — unit, integration, API, and security tests.

## API areas

Expected areas include cases, audio, transcripts, claims, reviews, civic guidance, reports, and health/readiness checks. Confirm exact routes and schemas in the implemented API reference.

## Core requirements

- Enforce authorization server-side on every case and file operation.
- Validate incoming and outgoing structured data.
- Track provenance for model outputs, human edits, and official-source citations.
- Use safe upload limits, content-type checks, storage permissions, and retention controls.
- Record material review and export actions without copying sensitive content into logs.
- Return explicit errors when a model or retrieval service is unavailable; never fabricate results.
- Keep secrets in environment or secret-management systems, never in source control.

Tests should cover permission boundaries, schema validation, source attribution, audit events, file handling, model-service failures, and report exports. Use synthetic fixtures by default.
