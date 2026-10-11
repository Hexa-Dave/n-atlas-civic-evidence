# Data dictionary

## Entities

| Entity | Key fields | Notes |
| --- | --- | --- |
| Case | `id`, `title`, `consent_recorded`, `status`, `created_at` | `status`: draft, in_review, finalized, archived |
| AudioAsset | `id`, `case_id`, `filename`, `content_type`, `storage_key`, `sha256` | Never store raw audio in Git |
| Transcript | `id`, `case_id`, `audio_asset_id`, `language`, `created_at` | Contains segments with speaker/time |
| Claim | `id`, `case_id`, `transcript_id`, `source_segment_id`, `text`, `status`, `confidence` | Always bound to a source segment |
| ReviewEvent | `id`, `claim_id`, `reviewer_id`, `decision`, `note`, `created_at` | Append-only |
| ModelRun | `id`, `task`, `model_id`, `model_version`, `config_json` | Records exact model identity |

## Status values

- Claim: `unverified`, `accepted`, `edited`, `rejected`, `flagged`.
- Claim status begins as `unverified` and only changes through a reviewed event.

## Provenance

Every extracted item carries its model run and source segment. Official-source
citations carry a source id, title, and section. Testimony and guidance are never
merged into a single field.
