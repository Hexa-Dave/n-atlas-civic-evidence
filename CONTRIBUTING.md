# Contributing

Thanks for helping build N-ATLAS Civic Evidence. This project handles sensitive
testimony and civic incident material, so contributions must preserve source
attribution, human review, and data-protection guarantees.

## Ground rules

- Never present a model-extracted allegation as a verified fact.
- Keep witness statements and official procedural guidance in separate fields.
- Do not commit real interview audio, personal data, credentials, or unapproved
  model weights. Use synthetic or redacted fixtures in tests.
- Mark proposed behavior as planned; distinguish measured results from targets.

## Development setup

1. Install the backend package: `make install` (see the `Makefile`).
2. Copy `.env.example` to `.env` and fill in local values. Never commit `.env`.
3. Run the database migrations and seed demo data.
4. Run `make test` and `make lint` before opening a change.

## Pull requests

- Keep changes focused and describe the safety impact of new behavior.
- Add or update tests for permission boundaries, schema validation, provenance,
  and model-service failure handling.
- Update the relevant `docs/` page when behavior or interfaces change.
- Reference the exact N-ATLAS model/version when a change depends on it.

## Reporting issues

Do not include private data, transcripts, or credentials in an issue. Describe
the problem with synthetic examples.
