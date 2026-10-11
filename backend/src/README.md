# Backend source tree

This directory contains the Python application package and implementation modules.

Organize source by responsibility: API transport, domain schemas, persistence models, services, processing pipelines, storage, security, and audit handling. Avoid putting all business logic in route handlers.

When adding a feature:
1. Define and validate its request/response contract.
2. Put domain behavior in a service or pipeline module.
3. Enforce authorization and record required audit events.
4. Add unit and API/integration tests.
5. Update the API reference and data dictionary.

Do not store real secrets, private interviews, generated reports, or large model files in this source tree.
