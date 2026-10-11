# Privacy and security

## Data protection

- Collect the minimum personal data needed to document a case.
- Never commit interview audio, transcripts, credentials, or private datasets.
- Store audio and documents in access-controlled storage, not in the repository.
- Apply retention and deletion controls; confirm deletion in the backend, not the UI.

## Access control

- Enforce authorization server-side on every case, file, and export operation.
- Scope queries by the authenticated actor; never trust client-supplied ids.
- Require a reviewer role to record review decisions.

## Handling model output

- Treat model output as untrusted input; validate against the JSON schemas.
- Keep extracted claims marked `unverified` until a human reviewer acts.
- Do not log sensitive content; log identifiers and action metadata only.

## Incident handling

Record material actions in the audit trail. If a secret or private dataset is
exposed, rotate the credential and follow the project's incident process.
