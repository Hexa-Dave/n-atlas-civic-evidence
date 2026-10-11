# N-ATLAS Civic Evidence

N-ATLAS Civic Evidence is a proposed civic-literacy and evidence-processing platform designed to help authorized users organize interview testimony and civic incident reports into reviewable, source-linked records.

The system supports documentation; it does **not** determine whether an allegation is true. Extracted claims remain attributed to their source and should be marked **unverified** unless independently corroborated. Official procedural guidance must be kept distinct from witness statements.

## Project status

This repository structure describes the intended implementation. Do not assume that N-ATLAS access, fine-tuning, benchmark results, production deployment, or real-world validation exist until supported by reproducible artifacts and evidence.

## Core workflow

1. Capture a report and record consent and handling permissions.
2. Transcribe audio where a supported speech-to-text path is available.
3. Use N-ATLAS to extract and classify claims into a validated structured format.
4. Link each extracted item to transcript text and, where available, audio time ranges.
5. Have an authorized human reviewer confirm, edit, reject, or flag each item.
6. Retrieve relevant official civic/legal procedural sources separately from testimony.
7. Export a report with provenance, review status, and source references.

## Repository map

- `apps/web/` — reviewer-facing web application.
- `backend/` — API, application services, persistence, authorization, and audit trail.
- `ml/` — N-ATLAS integration, fine-tuning, and evaluation.
- `data/` — schemas, annotations, splits, and benchmark manifests; private raw data stays out of Git.
- `civic_knowledge/` — curated official-source registry, ingestion, retrieval, and evaluation.
- `docs/` — architecture, user, model, benchmark, security, and deployment documentation.
- `infra/` — container, deployment, monitoring, and operational configuration.
- `scripts/` — repeatable developer and verification commands.
- `artifacts/` — generated model/evaluation outputs; generally excluded from Git.
- `submission/` — challenge demo, team profile, and evidence checklist.

## Safety and trust principles

- Never label an allegation as a verified fact solely because a model extracted it.
- Preserve source attribution and provenance for every claim.
- Keep testimony and official procedural information in separate fields and report sections.
- Require human review before finalizing or exporting consequential reports.
- Minimize personal data; restrict access and log sensitive actions.
- Do not commit confidential interviews, credentials, private datasets, or unapproved model weights.

## Development

See `docs/` for setup and implementation guides. Supply configuration through environment variables; copy `.env.example` to a local `.env` and never commit secrets.

## Production hardening requirements

The backend now enforces a few key production checks before startup:
- `APP_ENV=production` requires a strong `SECRET_KEY` (32+ characters)
- demo auth must be disabled in production
- production requires a non-SQLite database URL
- explicit, non-wildcard CORS origins are required

This keeps default local-dev behavior usable while preventing accidental unsafe configuration from shipping to production.

Before describing a capability as complete, verify it with tests and record evidence. Document the exact N-ATLAS model/version and access method, dataset provenance, held-out benchmark methodology, base-versus-fine-tuned results, and deployment verification.
