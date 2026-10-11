# API reference

Base path: `/api`. The API is versioned under `/v1`.

## Health

- `GET /healthz` - liveness.
- `GET /readyz` - readiness (database and model-service connectivity).

## Cases

- `GET /v1/cases` - list authorized cases.
- `POST /v1/cases` - create a case (records consent).
- `GET /v1/cases/{case_id}` - case detail.
- `DELETE /v1/cases/{case_id}` - delete/retain per policy.

## Audio and transcripts

- `POST /v1/cases/{case_id}/audio` - upload permitted audio.
- `GET /v1/cases/{case_id}/audio` - list audio assets.
- `POST /v1/cases/{case_id}/transcripts` - start transcription.
- `GET /v1/cases/{case_id}/transcripts/{transcript_id}` - retrieve transcript.

## Claims and reviews

- `POST /v1/cases/{case_id}/claims/extract` - extract claims via N-ATLAS.
- `GET /v1/cases/{case_id}/claims` - list claims.
- `PATCH /v1/cases/{case_id}/claims/{claim_id}` - edit a claim.
- `POST /v1/claims/{claim_id}/reviews` - record a reviewer decision.
- `GET /v1/claims/{claim_id}/reviews` - review history.

## Civic guidance and reports

- `GET /v1/civic-guidance/search` - retrieve official-source excerpts.
- `POST /v1/cases/{case_id}/reports` - generate a report.
- `GET /v1/cases/{case_id}/reports/{report_id}` - retrieve a report.

Exact request and response bodies are defined in `backend/src/civic_evidence/schemas/`.
Routes marked `501 Not Implemented` in the scaffold are not yet functional.
