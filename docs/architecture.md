# Architecture

## Purpose

N-ATLAS Civic Evidence turns interview testimony and civic incident reports into
reviewable, source-linked records. It documents; it does not establish truth.

## Components

- **Web app (`apps/web/`)** - reviewer interface.
- **Backend (`backend/`)** - API, services, persistence, authorization, audit.
- **ML (`ml/`)** - N-ATLAS integration, fine-tuning, and evaluation.
- **Civic knowledge (`civic_knowledge/`)** - official-source registry and retrieval.
- **Data (`data/`)** - schemas, annotations, splits, and benchmark manifest.

## Data flow

1. A case is created with consent and handling permissions recorded.
2. Audio is uploaded, validated, hashed, and stored.
3. A supported speech-to-text path produces a transcript with segments.
4. N-ATLAS extracts structured claims bound to segment ids.
5. A human reviewer accepts, edits, rejects, or flags each claim.
6. Relevant official sources are retrieved separately from testimony.
7. A report is assembled with provenance and review status, then exported.

## Boundaries

- The backend is the source of truth for permissions and case state.
- Testimony and official guidance are stored in separate fields and sections.
- Model output is decision support only; human review is required before finalizing.
