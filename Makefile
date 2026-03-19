SHELL := /bin/bash

.PHONY: frontend-install frontend-dev frontend-lint frontend-typecheck frontend-build
.PHONY: backend-install backend-dev backend-lint backend-test

frontend-install:
	cd frontend && npm install

frontend-dev:
	cd frontend && npm run dev

frontend-lint:
	cd frontend && npm run lint

frontend-typecheck:
	cd frontend && npm run typecheck

frontend-build:
	cd frontend && npm run build

backend-install:
	cd backend && python3 -m pip install -e ".[dev]"

backend-dev:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

backend-lint:
	cd backend && python3 -m ruff check .

backend-test:
	cd backend && pytest
