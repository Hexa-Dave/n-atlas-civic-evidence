# Infrastructure and operations

This directory contains deployment and operational assets.

## Intended contents

- `docker/` — container build definitions.
- `deployment/` — environment-specific deployment manifests and configuration templates.
- `monitoring/` — health checks, metrics, dashboards, and alert rules.
- `scripts/` — setup, migration, release, and verification scripts.

## Operational requirements

- Keep secrets in an approved secret store or deployment environment, never in Git.
- Separate development, staging, and production configuration.
- Use least-privilege service accounts and private storage for sensitive material.
- Provide health/readiness checks and logs that avoid exposing transcripts or personal data.
- Document backup, restoration, retention, deletion, and incident-response procedures.
- Pin and review dependencies and container base images.
- Verify deployment with automated checks and a documented smoke test.

Only describe a deployment as live after it has been deployed and independently verified.
