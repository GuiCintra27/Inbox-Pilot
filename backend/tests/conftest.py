from __future__ import annotations

from types import SimpleNamespace

import pytest

import app.services.analysis as analysis_module


@pytest.fixture(autouse=True)
def force_no_provider_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        analysis_module,
        "get_settings",
        lambda: SimpleNamespace(
            gemini_api_key="",
            gemini_model="gemini-2.5-flash",
            openrouter_api_key="",
            openrouter_model="google/gemini-2.0-flash-001",
        ),
    )
