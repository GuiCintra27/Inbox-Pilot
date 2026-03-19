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

## Phase 2 contract notes

- The analysis endpoint contract is defined in `docs/projects/TECHNICAL-REFERENCE.md`.
- The expected precedence for mixed input is `email_file` over `email_text`.
- The `provider` field identifies the active analysis engine; in Phase 2 it is a preview identifier, not the final external AI provider.
- Contract tests for `POST /analyze` live under `backend/tests/` and document the supported happy paths and failure modes of the current API.
