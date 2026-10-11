# Workflow

## Roles

- **Intake** - creates a case and records consent.
- **Reviewer** - confirms, edits, rejects, or flags extracted claims.
- **Publisher** - exports a finalized report.

## End-to-end flow

1. Intake records consent and handling permissions for a case.
2. Permitted audio or a written report is added to the case.
3. The system transcribes audio (when a supported path exists) or reads the report.
4. N-ATLAS extracts claims and classifications into validated structured records.
5. Each item is linked to its transcript segment and, where available, audio range.
6. A reviewer decides on each item and may add a note.
7. The system retrieves official procedural sources separately from testimony.
8. A report is assembled and exported, preserving review status and citations.

## Rules

- A claim stays `unverified` until a human reviewer acts on it.
- A report cannot be finalized with zero human-reviewed claims.
- When a model or retrieval service is unavailable, the step fails explicitly
  rather than producing invented content.
