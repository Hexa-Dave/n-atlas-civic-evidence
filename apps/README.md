# Applications

This directory contains user-facing applications for N-ATLAS Civic Evidence.

## Intended contents

- `web/` — the browser-based application for case intake, transcript review, claim review, civic guidance, and report export.
- Additional clients, if needed, should live in separate application directories.

## Boundary

Applications present information and collect user decisions. Business rules, authorization, durable storage, audit logging, model calls, and official-source retrieval belong in backend services.

## Expectations

- Use the typed API client rather than duplicating API logic in UI components.
- Show provenance and review status wherever extracted claims are displayed.
- Distinguish testimony, model extraction, human edits, and official sources.
- Provide accessible audio playback, transcript navigation, and keyboard operation.
- Never display model-generated allegations as established facts.
