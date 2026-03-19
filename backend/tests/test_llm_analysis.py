from __future__ import annotations

import json

import pytest

from app.domain.ingestion import IngestedContent
from app.schemas import Category
from app.services.llm_analysis import (
    ExternalResponseValidationError,
    GeminiAnalysisProvider,
    OpenRouterAnalysisProvider,
)

SAMPLE_CONTENT = IngestedContent(
    text="Please approve the invoice today and confirm the status.",
    source="text",
    language="en-US",
    language_confidence=0.92,
)


def test_gemini_provider_parses_successful_response() -> None:
    provider = GeminiAnalysisProvider(
        api_key="test-key",
        model="gemini-2.5-flash",
        transport=lambda _payload: {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": json.dumps(
                                    {
                                "category": "Produtivo",
                                "confidence": 0.93,
                                "rationale": "The email requests operational approval.",
                                "suggested_reply": (
                                    "Hello, we will review the invoice today."
                                ),
                                "keywords": ["invoice", "approval", "status"],
                            }
                        )
                    }
                        ]
                    }
                }
            ]
        },
    )

    result = provider.analyze(SAMPLE_CONTENT)

    assert result.provider == "gemini:gemini-2.5-flash"
    assert result.category == Category.productive
    assert result.confidence == 0.93


def test_gemini_provider_rejects_invalid_payload() -> None:
    provider = GeminiAnalysisProvider(
        api_key="test-key",
        model="gemini-2.5-flash",
        transport=lambda _payload: {
            "candidates": [{"content": {"parts": [{"text": '{"category":"Talvez"}'}]}}]
        },
    )

    with pytest.raises(ExternalResponseValidationError):
        provider.analyze(SAMPLE_CONTENT)


def test_openrouter_provider_parses_successful_response() -> None:
    provider = OpenRouterAnalysisProvider(
        api_key="test-key",
        model="google/gemini-2.0-flash-001",
        transport=lambda _payload: {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "category": "Improdutivo",
                                "confidence": 0.88,
                                "rationale": "The message is purely social.",
                                "suggested_reply": "Hello, thank you for your message.",
                                "keywords": ["thanks", "greetings"],
                            }
                        )
                    }
                }
            ]
        },
    )

    result = provider.analyze(SAMPLE_CONTENT)

    assert result.provider == "openrouter:google/gemini-2.0-flash-001"
    assert result.category == Category.unproductive
