# Backend

FastAPI backend for Inbox Pilot.

## Run locally

```bash
make setup
make backend-dev
```

Se você já tinha um `backend/.env` antigo e quiser recriar o arquivo a partir do exemplo atual:

```bash
make env-reset
```

O fluxo recomendado usa a virtualenv `.venv/` criada na raiz do projeto. Se preferir rodar manualmente:

```bash
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
cd backend
../.venv/bin/pip install -e ".[dev]"
../.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Use `backend/.env.example` como ponto de partida para configuração local. O caminho de AI é controlado por:

- `GEMINI_API_KEY`
- `GEMINI_MODEL`
- `OPENROUTER_API_KEY`
- `OPENROUTER_MODEL`

## Health check

```bash
curl http://localhost:8000/health
```

## Ingestion behavior

- When both `email_text` and `email_file` are provided, the uploaded file takes precedence.
- Empty uploads are rejected instead of falling back to the text field.
- Supported file types are `.txt` and `.pdf`.
- Input text is normalized before the analysis layer consumes it.
- Empty or unsupported uploads raise ingestion errors instead of silently falling back to another source.

## Phase 4 analysis contract

The analysis endpoint contract is defined in `docs/projects/TECHNICAL-REFERENCE.md`.

The `provider` field is part of the public payload and identifies the path that produced the response.

Documented provider values for the AI/fallback phase:

- `gemini:<model>` for a successful Gemini response
- `openrouter:<model>` when OpenRouter answers after Gemini is unavailable or fails
- `fallback:no-provider-key` when no external provider key is configured
- `fallback:provider-error` when the external providers fail
- `fallback:invalid-response` when the external providers return an invalid payload

Contract tests for `POST /analyze` live under `backend/tests/` and document the supported happy paths and failure modes of the current API.
