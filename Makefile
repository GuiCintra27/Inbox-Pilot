SHELL := /bin/bash

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn
RUFF := $(VENV)/bin/ruff
PYTEST := $(VENV)/bin/pytest
VENV_STAMP := $(VENV)/.ready

.PHONY: setup env-init env-reset frontend-install frontend-dev frontend-reset frontend-lint frontend-typecheck frontend-build
.PHONY: backend-install backend-dev backend-lint backend-test

frontend-install:
	cd frontend && npm install

frontend-dev:
	./scripts/frontend-dev.sh

frontend-reset:
	rm -rf frontend/.next frontend/tsconfig.tsbuildinfo

frontend-lint:
	cd frontend && npm run lint

frontend-typecheck:
	cd frontend && npm run typecheck

frontend-build:
	cd frontend && npm run build

$(VENV_STAMP):
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	touch $(VENV_STAMP)

env-init:
	@if [ ! -f frontend/.env.local ]; then cp frontend/.env.example frontend/.env.local; fi
	@if [ ! -f backend/.env ]; then cp backend/.env.example backend/.env; fi

env-reset:
	cp frontend/.env.example frontend/.env.local
	cp backend/.env.example backend/.env

setup: env-init frontend-install backend-install

backend-install: $(VENV_STAMP)
	cd backend && ../$(PIP) install -e ".[dev]"

backend-dev: $(VENV_STAMP)
	cd backend && ../$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000

backend-lint: $(VENV_STAMP)
	cd backend && ../$(RUFF) check .

backend-test: $(VENV_STAMP)
	cd backend && ../$(PYTEST)
