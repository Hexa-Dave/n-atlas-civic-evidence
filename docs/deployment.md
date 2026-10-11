# Deployment

## Configuration

All configuration is supplied through environment variables. Copy `.env.example`
to `.env` for local use and never commit a populated `.env`.

## Local

```
make install
cp .env.example .env
docker compose up --build
```

- Backend: `http://localhost:8000` (docs at `/docs`).
- Web: `http://localhost:3000`.

## Migrations and seed data

```
make migrate
make seed
```

## Verification

Run `python scripts/verify_deployment.py` against a deployed environment to check
health, readiness, and basic authorization behavior. A successful upload or a
running container alone is not proof the system works.

## Production notes

- Store secrets in a secret manager, not in the image or repository.
- Terminate TLS in front of the backend and restrict CORS to the web origin.
- Back up the database and document the restore procedure.
