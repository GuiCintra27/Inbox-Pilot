from __future__ import annotations

from types import SimpleNamespace

from app.domain.ingestion import IngestedContent
from app.schemas import Category
from app.services.analysis import analyze_ingested_content
from app.services.fallback_analysis import (
    FALLBACK_PROVIDER_INVALID_RESPONSE,
    FALLBACK_PROVIDER_NO_OPENAI_KEY,
    FALLBACK_PROVIDER_PROVIDER_ERROR,
)
from app.services.openai_analysis import (
    OpenAIAnalysisResult,
    OpenAIProviderError,
    OpenAIResponseValidationError,
)

SAMPLE_CONTENT = IngestedContent(
    text="Please approve the invoice today and confirm the status.",
    source="text",
    language="en-US",
    language_confidence=0.92,
)


def test_analyze_ingested_content_uses_openai_when_available() -> None:
    class FakeProvider:
        def __init__(self, *, api_key: str, model: str) -> None:
            self.api_key = api_key
            self.model = model

        def analyze(self, ingested_content: IngestedContent) -> OpenAIAnalysisResult:
            return OpenAIAnalysisResult(
                category=Category.productive,
                confidence=0.97,
                rationale="A mensagem pede uma atualização operacional.",
                suggested_reply=(
                    "Olá! Recebemos sua solicitação e vamos revisar os próximos passos."
                ),
                keywords=["solicitação", "atualização"],
                provider="openai:gpt-5-mini",
            )

    result = analyze_ingested_content(
        SAMPLE_CONTENT,
        settings=SimpleNamespace(
            openai_api_key="test-openai-key",
            openai_model="gpt-5-mini",
        ),
        provider_factory=FakeProvider,
    )

    assert result.provider == "openai:gpt-5-mini"
    assert result.category == Category.productive
    assert result.confidence == 0.97


def test_analyze_ingested_content_uses_fallback_without_openai_key() -> None:
    result = analyze_ingested_content(
        SAMPLE_CONTENT,
        settings=SimpleNamespace(
            openai_api_key="",
            openai_model="gpt-5-mini",
        ),
    )

    assert result.provider == FALLBACK_PROVIDER_NO_OPENAI_KEY
    assert result.category in {Category.productive, Category.unproductive}


def test_analyze_ingested_content_uses_fallback_on_provider_error() -> None:
    class FakeProvider:
        def __init__(self, *, api_key: str, model: str) -> None:
            self.api_key = api_key
            self.model = model

        def analyze(self, ingested_content: IngestedContent) -> OpenAIAnalysisResult:
            raise OpenAIProviderError("provider unavailable")

    result = analyze_ingested_content(
        SAMPLE_CONTENT,
        settings=SimpleNamespace(
            openai_api_key="test-openai-key",
            openai_model="gpt-5-mini",
        ),
        provider_factory=FakeProvider,
    )

    assert result.provider == FALLBACK_PROVIDER_PROVIDER_ERROR
    assert result.category in {Category.productive, Category.unproductive}


def test_analyze_ingested_content_uses_fallback_on_invalid_response() -> None:
    class FakeProvider:
        def __init__(self, *, api_key: str, model: str) -> None:
            self.api_key = api_key
            self.model = model

        def analyze(self, ingested_content: IngestedContent) -> OpenAIAnalysisResult:
            raise OpenAIResponseValidationError("schema mismatch")

    result = analyze_ingested_content(
        SAMPLE_CONTENT,
        settings=SimpleNamespace(
            openai_api_key="test-openai-key",
            openai_model="gpt-5-mini",
        ),
        provider_factory=FakeProvider,
    )

    assert result.provider == FALLBACK_PROVIDER_INVALID_RESPONSE
    assert result.category in {Category.productive, Category.unproductive}
