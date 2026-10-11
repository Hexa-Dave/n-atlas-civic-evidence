#!/usr/bin/env bash
# Run the backend and web app together for local development.
set -euo pipefail

docker compose up --build
