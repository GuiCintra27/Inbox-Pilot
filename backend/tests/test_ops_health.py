from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest
from fastapi import HTTPException, Response
from starlette.requests import Request

from app.api.analyze import analyze_email
from app.api.ops import audit_trail_snapshot, llm_health, require_ops_access


def _build_request() -> Request:
    return _build_ops_request()


def _build_ops_request(
    *,
    client_host: str = "127.0.0.1",
    headers: dict[str, str] | None = None,
) -> Request:
    encoded_headers = [
        (key.lower().encode("latin-1"), value.encode("latin-1"))
        for key, value in (headers or {}).items()
    ]
    scope = {
        "type": "http",
        "headers": encoded_headers,
        "client": (client_host, 12345),
        "method": "POST",
        "path": "/analyze",
    }
    return Request(scope)


def test_ops_llm_health_reports_operational_snapshot() -> None:
    asyncio.run(
        analyze_email(
            request=_build_request(),
            response=Response(),
            email_text="Please confirm the invoice status today.",
            email_file=None,
        )
    )

    payload = asyncio.run(llm_health())

    assert "providers" in payload
    assert "circuit_breakers" in payload
    assert "requests" in payload
    assert "fallbacks" in payload
    assert "redactions" in payload
    assert "rate_limits" in payload
    assert payload["requests"]["total"] == 1


def test_ops_audit_trail_reports_recent_events_without_sensitive_content() -> None:
    response = Response()
    asyncio.run(
        analyze_email(
            request=_build_request(),
            response=response,
            email_text="Contato maria@example.com e pedido 9981 para follow-up imediato.",
            email_file=None,
        )
    )

    payload = asyncio.run(audit_trail_snapshot())

    assert payload["count"] == 1
    assert payload["retention_mode"] == "zero_content_retention"
    event = payload["events"][0]
    assert "request_id" in event
    assert "provider_attempts" in event
    assert "maria@example.com" not in str(event)
    assert "pedido 9981" not in str(event)


def test_ops_endpoints_allow_loopback_in_local(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = SimpleNamespace(
        app_env="local",
        ops_endpoints_enabled=True,
        ops_auth_header="X-Ops-Token",
        ops_access_token="secret",
    )
    monkeypatch.setattr("app.api.ops.get_settings", lambda: settings)

    require_ops_access(_build_ops_request(client_host="127.0.0.1"))


def test_ops_endpoints_reject_non_loopback_in_local(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = SimpleNamespace(
        app_env="local",
        ops_endpoints_enabled=True,
        ops_auth_header="X-Ops-Token",
        ops_access_token="secret",
    )
    monkeypatch.setattr("app.api.ops.get_settings", lambda: settings)

    with pytest.raises(HTTPException) as exc_info:
        require_ops_access(_build_ops_request(client_host="10.0.0.8"))

    assert exc_info.value.status_code == 403


def test_ops_endpoints_return_404_when_disabled_outside_local(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = SimpleNamespace(
        app_env="production",
        ops_endpoints_enabled=False,
        ops_auth_header="X-Ops-Token",
        ops_access_token="secret",
    )
    monkeypatch.setattr("app.api.ops.get_settings", lambda: settings)

    with pytest.raises(HTTPException) as exc_info:
        require_ops_access(_build_ops_request(client_host="10.0.0.8"))

    assert exc_info.value.status_code == 404


def test_ops_endpoints_return_404_when_token_missing_from_config(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = SimpleNamespace(
        app_env="production",
        ops_endpoints_enabled=True,
        ops_auth_header="X-Ops-Token",
        ops_access_token="",
    )
    monkeypatch.setattr("app.api.ops.get_settings", lambda: settings)

    with pytest.raises(HTTPException) as exc_info:
        require_ops_access(_build_ops_request(client_host="10.0.0.8"))

    assert exc_info.value.status_code == 404


def test_ops_endpoints_return_403_with_wrong_token(monkeypatch: pytest.MonkeyPatch) -> None:
    settings = SimpleNamespace(
        app_env="production",
        ops_endpoints_enabled=True,
        ops_auth_header="X-Ops-Token",
        ops_access_token="secret",
    )
    monkeypatch.setattr("app.api.ops.get_settings", lambda: settings)

    with pytest.raises(HTTPException) as exc_info:
        require_ops_access(
            _build_ops_request(client_host="10.0.0.8", headers={"X-Ops-Token": "wrong"})
        )

    assert exc_info.value.status_code == 403


def test_ops_endpoints_allow_correct_token_outside_local(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = SimpleNamespace(
        app_env="production",
        ops_endpoints_enabled=True,
        ops_auth_header="X-Ops-Token",
        ops_access_token="secret",
    )
    monkeypatch.setattr("app.api.ops.get_settings", lambda: settings)

    require_ops_access(
        _build_ops_request(client_host="10.0.0.8", headers={"X-Ops-Token": "secret"})
    )
