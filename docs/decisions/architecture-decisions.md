# Architecture decision records

Record each significant decision with context, options, decision, and
consequences. Newest first.

## ADR-0001: Keep testimony and civic guidance strictly separate

- **Context:** Reports mix witness statements with procedural information.
- **Decision:** Store and render testimony and official guidance in separate
  fields and report sections.
- **Consequences:** No field ever merges the two; retrieval cannot source-flood a
  testimony section.

## ADR-0002: Human review required before finalizing a report

- **Context:** Model output can be wrong or unsupported.
- **Decision:** A report cannot be finalized with zero human-reviewed claims.
- **Consequences:** The review workflow is on the critical path for exports.

## ADR-0003: Validate model output against JSON schemas

- **Context:** Model output is untrusted.
- **Decision:** Reject or quarantine records that fail schema validation.
- **Consequences:** Invalid output never reaches persistence or the reviewer UI.
