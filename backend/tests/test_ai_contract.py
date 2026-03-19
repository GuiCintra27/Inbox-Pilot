from __future__ import annotations

from types import SimpleNamespace

from app.domain.ingestion import IngestedContent
from app.schemas import Category
from app.services.analysis import analyze_ingested_content
from app.services.fallback_analysis import (
    FALLBACK_PROVIDER_INVALID_RESPONSE,
    FALLBACK_PROVIDER_NO_PROVIDER_KEY,
    FALLBACK_PROVIDER_PROVIDER_ERROR,
)
from app.services.llm_analysis import (
    ExternalAnalysisResult,
    ExternalProviderError,
    ExternalResponseValidationError,
)

SAMPLE_CONTENT = IngestedContent(
    text="Please approve the invoice today and confirm the status.",
    source="text",
    language="en-US",
    language_confidence=0.92,
)


def test_analyze_ingested_content_uses_gemini_when_available() -> None:
    class FakeGeminiProvider:
        def __init__(self, *, api_key: str, model: str) -> None:
            self.api_key = api_key
            self.model = model

        def analyze(self, ingested_content: IngestedContent) -> ExternalAnalysisResult:
            return ExternalAnalysisResult(
                category=Category.productive,
                confidence=0.97,
                rationale="A mensagem pede uma atualização operacional.",
                suggested_reply=(
                    "Olá! Recebemos sua solicitação e vamos revisar os próximos passos."
                ),
                keywords=["solicitação", "atualização"],
                provider="gemini:gemini-2.5-flash",
            )

    result = analyze_ingested_content(
        SAMPLE_CONTENT,
        settings=SimpleNamespace(
            gemini_api_key="test-gemini-key",
            gemini_model="gemini-2.5-flash",
            openrouter_api_key="",
            openrouter_model="google/gemini-2.0-flash-001",
        ),
        gemini_provider_factory=FakeGeminiProvider,
    )

    assert result.provider == "gemini:gemini-2.5-flash"
    assert result.category == Category.productive
    assert result.confidence == 0.97


def test_analyze_ingested_content_uses_openrouter_when_gemini_is_unavailable() -> None:
    class FakeOpenRouterProvider:
        def __init__(self, *, api_key: str, model: str) -> None:
            self.api_key = api_key
            self.model = model

        def analyze(self, ingested_content: IngestedContent) -> ExternalAnalysisResult:
            return ExternalAnalysisResult(
                category=Category.productive,
                confidence=0.91,
                rationale="A mensagem pede acompanhamento operacional.",
                suggested_reply="Olá! Vamos revisar e retornar em breve.",
                keywords=["status", "ticket"],
                provider="openrouter:google/gemini-2.0-flash-001",
            )

    result = analyze_ingested_content(
        SAMPLE_CONTENT,
        settings=SimpleNamespace(
            gemini_api_key="",
            gemini_model="gemini-2.5-flash",
            openrouter_api_key="test-openrouter-key",
            openrouter_model="google/gemini-2.0-flash-001",
        ),
        openrouter_provider_factory=FakeOpenRouterProvider,
    )

    assert result.provider == "openrouter:google/gemini-2.0-flash-001"
    assert result.category == Category.productive


def test_analyze_ingested_content_uses_fallback_without_provider_key() -> None:
    result = analyze_ingested_content(
        SAMPLE_CONTENT,
        settings=SimpleNamespace(
            gemini_api_key="",
            gemini_model="gemini-2.5-flash",
            openrouter_api_key="",
            openrouter_model="google/gemini-2.0-flash-001",
        ),
    )

    assert result.provider == FALLBACK_PROVIDER_NO_PROVIDER_KEY
    assert result.category in {Category.productive, Category.unproductive}


def test_analyze_ingested_content_uses_fallback_on_provider_error() -> None:
    class FailingGeminiProvider:
        def __init__(self, *, api_key: str, model: str) -> None:
            self.api_key = api_key
            self.model = model

        def analyze(self, ingested_content: IngestedContent) -> ExternalAnalysisResult:
            raise ExternalProviderError("provider unavailable")

    result = analyze_ingested_content(
        SAMPLE_CONTENT,
        settings=SimpleNamespace(
            gemini_api_key="test-gemini-key",
            gemini_model="gemini-2.5-flash",
            openrouter_api_key="",
            openrouter_model="google/gemini-2.0-flash-001",
        ),
        gemini_provider_factory=FailingGeminiProvider,
    )

    assert result.provider == FALLBACK_PROVIDER_PROVIDER_ERROR
    assert result.category in {Category.productive, Category.unproductive}


def test_analyze_ingested_content_uses_fallback_on_invalid_response() -> None:
    class InvalidGeminiProvider:
        def __init__(self, *, api_key: str, model: str) -> None:
            self.api_key = api_key
            self.model = model

        def analyze(self, ingested_content: IngestedContent) -> ExternalAnalysisResult:
            raise ExternalResponseValidationError("schema mismatch")

    result = analyze_ingested_content(
        SAMPLE_CONTENT,
        settings=SimpleNamespace(
            gemini_api_key="test-gemini-key",
            gemini_model="gemini-2.5-flash",
            openrouter_api_key="",
            openrouter_model="google/gemini-2.0-flash-001",
        ),
        gemini_provider_factory=InvalidGeminiProvider,
    )

    assert result.provider == FALLBACK_PROVIDER_INVALID_RESPONSE
    assert result.category in {Category.productive, Category.unproductive}


def test_analyze_ingested_content_uses_openrouter_after_gemini_failure() -> None:
    class FailingGeminiProvider:
        def __init__(self, *, api_key: str, model: str) -> None:
            self.api_key = api_key
            self.model = model

        def analyze(self, ingested_content: IngestedContent) -> ExternalAnalysisResult:
            raise ExternalProviderError("gemini unavailable")

    class FakeOpenRouterProvider:
        def __init__(self, *, api_key: str, model: str) -> None:
            self.api_key = api_key
            self.model = model

        def analyze(self, ingested_content: IngestedContent) -> ExternalAnalysisResult:
            return ExternalAnalysisResult(
                category=Category.productive,
                confidence=0.9,
                rationale="OpenRouter recovered the request.",
                suggested_reply="Olá! Vamos seguir com a análise.",
                keywords=["request", "fallback"],
                provider="openrouter:google/gemini-2.0-flash-001",
            )

    result = analyze_ingested_content(
        SAMPLE_CONTENT,
        settings=SimpleNamespace(
            gemini_api_key="test-gemini-key",
            gemini_model="gemini-2.5-flash",
            openrouter_api_key="test-openrouter-key",
            openrouter_model="google/gemini-2.0-flash-001",
        ),
        gemini_provider_factory=FailingGeminiProvider,
        openrouter_provider_factory=FakeOpenRouterProvider,
    )

    assert result.provider == "openrouter:google/gemini-2.0-flash-001"
