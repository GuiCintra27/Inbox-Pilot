from __future__ import annotations

import asyncio

from app.api.analyze import health_check


def test_health() -> None:
    assert asyncio.run(health_check()) == {
        "status": "ok",
        "service": "inbox-pilot-backend",
    }
