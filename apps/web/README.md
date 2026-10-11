# Web application

The web client is the reviewer-facing interface for managing cases, reviewing transcripts and extracted claims, consulting civic guidance, and exporting reports.

## Planned areas

- `app/` — routes and page layouts.
- `components/` — reusable UI such as the audio player, transcript viewer, claim card, evidence timeline, review panel, and report preview.
- `hooks/` — reusable client-side state and data hooks.
- `lib/` — API client, authentication helpers, shared types, and UI utilities.

## Main user journeys

1. Sign in and open an authorized case.
2. Upload or access permitted audio and transcript material.
3. Compare extracted claims with transcript/audio context.
4. Accept, edit, reject, or flag claims and record a reviewer note.
5. Consult separately labeled civic/legal procedural sources.
6. Preview and export a report that preserves source links and review status.

## Implementation notes

- Treat the backend as the source of truth for permissions and case state.
- Never put secrets or privileged API keys in browser code.
- Display loading, failure, empty, and permission-denied states clearly.
- Keep transcript segments and claims navigable to their source context.
- Use labels such as `Model-extracted`, `Human-reviewed`, and `Unverified`.
- Do not claim an upload has been securely stored or deleted unless the backend confirms it.

Document the required Node.js version, package manager, environment variables, and test/build commands once finalized.
