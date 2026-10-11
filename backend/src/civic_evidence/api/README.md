# API routing

This directory groups HTTP API routes. Keep route handlers focused on request parsing, authorization dependencies, service invocation, and response mapping.

Expected versioned routes include `cases.py`, `audio.py`, `transcripts.py`, `claims.py`, `reviews.py`, `civic_guidance.py`, `reports.py`, and `health.py`.

The actual public contract must be documented in `docs/api/` and checked against implemented schemas. Do not expose internal file paths, credentials, private prompts, or unrestricted storage URLs through API responses.
