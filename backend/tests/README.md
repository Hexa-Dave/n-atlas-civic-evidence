# Backend tests

Backend tests protect application behavior, data integrity, and privacy boundaries.

## Suggested test groups

- `unit/` — schemas, services, validators, and isolated functions.
- `integration/` — database, storage, retrieval, and model-adapter interactions.
- `api/` — request/response behavior, status codes, authentication, and permissions.
- `security/` — cross-case access attempts, upload validation, log leakage, and export permissions.

Use synthetic or explicitly approved fixtures. Tests must not depend on live witness recordings or production credentials. Include negative tests: unauthorized users must not be able to read, edit, export, or infer the existence of another user's case.
