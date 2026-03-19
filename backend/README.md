# Backend

FastAPI backend for Inbox Pilot.

## Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Use `backend/.env.example` as the starting point for local configuration. The AI path is controlled by:

- `OPENAI_API_KEY`
- `OPENAI_MODEL`

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

- `openai:<model>` for a successful OpenAI response
- `fallback:no-openai-key` when the request uses the local fallback because no API key is available
- `fallback:provider-error` when the request uses the local fallback because the external provider failed
- `fallback:invalid-response` when the request uses the local fallback because the provider response could not be adapted to the contract

Contract tests for `POST /analyze` live under `backend/tests/` and document the supported happy paths and failure modes of the current API.
