#!/usr/bin/env bash
# Prepare a local development environment for N-ATLAS Civic Evidence.
set -euo pipefail

echo "Installing backend (editable) and web dependencies..."
python -m pip install -e ./backend
( cd apps/web && npm install )

if [ ! -f .env ]; then
  echo "Creating .env from .env.example (fill in real values before use)."
  cp .env.example .env
fi

echo "Setup complete. Run 'make migrate && make seed' next."
