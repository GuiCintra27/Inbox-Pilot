from __future__ import annotations

import json

import pytest

from app.domain.ingestion import IngestedContent
from app.schemas import Category
from app.services.openai_analysis import (
    OpenAIAnalysisProvider,
    OpenAIAnalysisResult,
    OpenAIProviderError,
    OpenAIResponseValidationError,
)


def _build_content() -> IngestedContent:
    return IngestedContent(
        text="Please approve the invoice today and confirm the status.",
        source="text",
        language="en-US",
        language_confidence=0.92,
    )


def test_openai_provider_returns_valid_result() -> None:
    captured_payload: dict[str, object] = {}

    def transport(request_payload: dict[str, object]) -> dict[str, object]:
        captured_payload.update(request_payload)
        response_body = json.dumps(
            {
                "category": "Produtivo",
                "confidence": 0.91,
                "rationale": "The email asks for an operational action.",
                "suggested_reply": "Hello, thanks for the update.",
                "keywords": ["invoice", "approve", "status"],
            }
        )
        return {
            "choices": [
                {
                    "message": {
                        "content": response_body,
                    }
                }
            ]
        }

    provider = OpenAIAnalysisProvider(
        api_key="test-api-key",
        model="gpt-5-mini",
        transport=transport,
    )

    result = provider.analyze(_build_content())

    assert captured_payload["model"] == "gpt-5-mini"
    assert captured_payload["response_format"] == {"type": "json_object"}
    assert result == OpenAIAnalysisResult(
        category=Category.productive,
        confidence=0.91,
        rationale="The email asks for an operational action.",
        suggested_reply="Hello, thanks for the update.",
        keywords=["invoice", "approve", "status"],
        provider="openai:gpt-5-mini",
    )


def test_openai_provider_rejects_invalid_payload() -> None:
    provider = OpenAIAnalysisProvider(
        api_key="test-api-key",
        model="gpt-5-mini",
        transport=lambda _payload: {
            "choices": [{"message": {"content": "{\"category\": \"unknown\"}"}}]
        },
    )

    with pytest.raises(OpenAIResponseValidationError):
        provider.analyze(_build_content())


def test_openai_provider_requires_api_key() -> None:
    provider = OpenAIAnalysisProvider(api_key=" ", model="gpt-5-mini")

    with pytest.raises(OpenAIProviderError):
        provider.analyze(_build_content())

