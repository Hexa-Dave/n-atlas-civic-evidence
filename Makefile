# N-ATLAS Civic Evidence - common developer commands.
# Requires GNU make. Use `make help` to list targets.

.DEFAULT_GOAL := help

.PHONY: help install dev backend-dev web-dev test lint migrate seed clean

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "%-14s %s\n", $$1, $$2}'

install: ## Install backend (editable) and web dependencies
	python -m pip install -e ./backend
	cd apps/web && npm install

dev: ## Run backend and web together via docker compose
	docker compose up --build

backend-dev: ## Run the backend locally with autoreload
	uvicorn civic_evidence.main:app --host 0.0.0.0 --port 8000 --reload

web-dev: ## Run the web app locally
	cd apps/web && npm run dev

test: ## Run backend and ML test suites
	python -m pytest backend/tests ml/tests
	cd apps/web && npm run typecheck

lint: ## Run formatting and static checks
	python -m ruff check backend ml civic_knowledge scripts
	cd apps/web && npm run typecheck

migrate: ## Apply database migrations
	cd backend && alembic upgrade head

seed: ## Load synthetic demo data
	python scripts/seed_demo_data.py

clean: ## Remove local caches and build artifacts
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache
