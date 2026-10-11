#!/usr/bin/env bash
# Run backend and ML test suites plus the web type check.
set -euo pipefail

python -m pytest backend/tests ml/tests civic_knowledge/evaluation
( cd apps/web && npm run typecheck )
