from __future__ import annotations

from types import SimpleNamespace

import pytest

import app.services.analysis as analysis_module


@pytest.fixture(autouse=True)
def force_no_openai_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        analysis_module,
        "get_settings",
        lambda: SimpleNamespace(openai_api_key="", openai_model="gpt-5-mini"),
    )
