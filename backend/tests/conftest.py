from __future__ import annotations

from types import SimpleNamespace

import pytest

import app.api.analyze as analyze_api_module
import app.services.analysis as analysis_module
import app.services.ingestion as ingestion_module
from app.core.security import reset_security_state


@pytest.fixture(autouse=True)
def force_no_provider_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    settings_stub = SimpleNamespace(
        gemini_api_key="",
        gemini_model="gemini-2.5-flash",
        openrouter_api_key="",
        openrouter_model="google/gemini-2.0-flash-001",
        max_provider_input_chars=8000,
        max_email_text_chars=12000,
        max_upload_bytes=1048576,
        max_pdf_pages=10,
        rate_limit_analyze_requests=20,
        rate_limit_window_seconds=60,
        provider_timeout_seconds=12,
        provider_retry_attempts=1,
        provider_retry_backoff_ms=0,
        circuit_breaker_failure_threshold=3,
        circuit_breaker_open_seconds=120,
        redaction_enabled=True,
        zero_content_retention=True,
        audit_trace_enabled=True,
        audit_recent_events_limit=200,
        audit_event_maxlen=120,
        audit_request_id_header="X-Request-ID",
        ops_endpoints_enabled=True,
        ops_auth_header="X-Ops-Token",
        ops_access_token="",
    )
    monkeypatch.setattr(
        analysis_module,
        "get_settings",
        lambda: settings_stub,
    )
    monkeypatch.setattr(analyze_api_module, "get_settings", lambda: settings_stub)
    monkeypatch.setattr(ingestion_module, "get_settings", lambda: settings_stub)


@pytest.fixture(autouse=True)
def reset_security_runtime() -> None:
    reset_security_state()
