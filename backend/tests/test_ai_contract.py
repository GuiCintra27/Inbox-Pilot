from __future__ import annotations

from types import SimpleNamespace

import app.services.analysis as analysis_module
from app.core.security import operational_metrics, provider_circuit_breakers
from app.domain.ingestion import IngestedContent
from app.schemas import Category
from app.services.analysis import analyze_ingested_content, analyze_ingested_content_with_trace
from app.services.fallback_analysis import (
    FALLBACK_PROVIDER_INVALID_RESPONSE,
    FALLBACK_PROVIDER_NO_PROVIDER_KEY,
    FALLBACK_PROVIDER_PROVIDER_ERROR,
)
from app.services.llm_analysis import (
    ExternalAnalysisResult,
    ExternalProviderError,
    ExternalResponseValidationError,
    ExternalTransportError,
)

SAMPLE_CONTENT = IngestedContent(
    text="Please approve the invoice today and confirm the status.",
    source="text",
    language="en-US",
    language_confidence=0.92,
)


def _settings_stub(**overrides: object) -> SimpleNamespace:
    defaults: dict[str, object] = {
        "gemini_api_key": "",
        "gemini_model": "gemini-2.5-flash",
        "openrouter_api_key": "",
        "openrouter_model": "google/gemini-2.0-flash-001",
        "max_provider_input_chars": 8000,
        "provider_timeout_seconds": 12,
        "provider_retry_attempts": 1,
        "provider_retry_backoff_ms": 0,
        "circuit_breaker_failure_threshold": 3,
        "circuit_breaker_open_seconds": 120,
        "redaction_enabled": True,
        "zero_content_retention": True,
        "audit_trace_enabled": True,
        "audit_recent_events_limit": 200,
        "audit_event_maxlen": 120,
        "audit_request_id_header": "X-Request-ID",
    }
    defaults.update(overrides)
    return SimpleNamespace(
        **defaults,
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
        settings=_settings_stub(gemini_api_key="test-gemini-key"),
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
        settings=_settings_stub(openrouter_api_key="test-openrouter-key"),
        openrouter_provider_factory=FakeOpenRouterProvider,
    )

    assert result.provider == "openrouter:google/gemini-2.0-flash-001"
    assert result.category == Category.productive


def test_analyze_ingested_content_uses_fallback_without_provider_key() -> None:
    result = analyze_ingested_content(
        SAMPLE_CONTENT,
        settings=_settings_stub(),
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
        settings=_settings_stub(gemini_api_key="test-gemini-key"),
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
        settings=_settings_stub(gemini_api_key="test-gemini-key"),
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
        settings=_settings_stub(
            gemini_api_key="test-gemini-key",
            openrouter_api_key="test-openrouter-key",
        ),
        gemini_provider_factory=FailingGeminiProvider,
        openrouter_provider_factory=FakeOpenRouterProvider,
    )

    assert result.provider == "openrouter:google/gemini-2.0-flash-001"


def test_analyze_ingested_content_redacts_provider_input_but_preserves_fallback_source(
    monkeypatch,
) -> None:
    observed_provider_text: dict[str, str] = {}
    observed_fallback_text: dict[str, str] = {}
    sensitive_content = IngestedContent(
        text=(
            "Contato: maria@example.com, telefone +55 11 99999-1234, "
            "CPF 123.456.789-09, pedido 9981 e ticket ABC-123."
        ),
        source="text",
        language="pt-BR",
        language_confidence=0.95,
    )

    class CapturingGeminiProvider:
        def __init__(self, *, api_key: str, model: str, timeout_seconds: float) -> None:
            self.api_key = api_key
            self.model = model
            self.timeout_seconds = timeout_seconds

        def analyze(self, ingested_content: IngestedContent) -> ExternalAnalysisResult:
            observed_provider_text["text"] = ingested_content.text
            raise ExternalProviderError("force fallback")

    def fake_fallback(*, ingested_content: IngestedContent, provider: str):
        observed_fallback_text["text"] = ingested_content.text
        return ExternalAnalysisResult(
            category=Category.productive,
            confidence=0.7,
            rationale="fallback",
            suggested_reply="fallback",
            keywords=["fallback"],
            provider=provider,
        )

    monkeypatch.setattr(analysis_module, "analyze_with_fallback", fake_fallback)

    result = analyze_ingested_content(
        sensitive_content,
        settings=_settings_stub(gemini_api_key="test-gemini-key"),
        gemini_provider_factory=CapturingGeminiProvider,
    )

    assert result.provider == FALLBACK_PROVIDER_PROVIDER_ERROR
    assert "[EMAIL]" in observed_provider_text["text"]
    assert "[PHONE]" in observed_provider_text["text"]
    assert "[CPF]" in observed_provider_text["text"]
    assert "[OP_ID]" in observed_provider_text["text"]
    assert "maria@example.com" not in observed_provider_text["text"]
    assert "123.456.789-09" not in observed_provider_text["text"]
    assert "pedido 9981" in observed_fallback_text["text"]
    assert "ticket ABC-123" in observed_fallback_text["text"]


def test_timeout_retries_once_then_falls_back_to_openrouter(monkeypatch) -> None:
    attempts = {"gemini": 0, "openrouter": 0}

    class TimeoutGeminiProvider:
        def __init__(self, *, api_key: str, model: str, timeout_seconds: float) -> None:
            self.api_key = api_key
            self.model = model
            self.timeout_seconds = timeout_seconds

        def analyze(self, ingested_content: IngestedContent) -> ExternalAnalysisResult:
            attempts["gemini"] += 1
            raise ExternalTransportError("timeout")

    class SuccessfulOpenRouterProvider:
        def __init__(self, *, api_key: str, model: str, timeout_seconds: float) -> None:
            self.api_key = api_key
            self.model = model
            self.timeout_seconds = timeout_seconds

        def analyze(self, ingested_content: IngestedContent) -> ExternalAnalysisResult:
            attempts["openrouter"] += 1
            return ExternalAnalysisResult(
                category=Category.productive,
                confidence=0.91,
                rationale="OpenRouter recovered the request.",
                suggested_reply="Olá! Vamos seguir com a análise.",
                keywords=["status", "timeout"],
                provider="openrouter:google/gemini-2.0-flash-001",
            )

    monkeypatch.setattr(analysis_module.time, "sleep", lambda _seconds: None)

    result = analyze_ingested_content(
        SAMPLE_CONTENT,
        settings=_settings_stub(
            gemini_api_key="test-gemini-key",
            openrouter_api_key="test-openrouter-key",
        ),
        gemini_provider_factory=TimeoutGeminiProvider,
        openrouter_provider_factory=SuccessfulOpenRouterProvider,
    )

    assert attempts["gemini"] == 2
    assert attempts["openrouter"] == 1
    assert result.provider == "openrouter:google/gemini-2.0-flash-001"


def test_invalid_response_does_not_retry_before_using_openrouter(monkeypatch) -> None:
    attempts = {"gemini": 0, "openrouter": 0}

    class InvalidGeminiProvider:
        def __init__(self, *, api_key: str, model: str, timeout_seconds: float) -> None:
            self.api_key = api_key
            self.model = model
            self.timeout_seconds = timeout_seconds

        def analyze(self, ingested_content: IngestedContent) -> ExternalAnalysisResult:
            attempts["gemini"] += 1
            raise ExternalResponseValidationError("schema mismatch")

    class SuccessfulOpenRouterProvider:
        def __init__(self, *, api_key: str, model: str, timeout_seconds: float) -> None:
            self.api_key = api_key
            self.model = model
            self.timeout_seconds = timeout_seconds

        def analyze(self, ingested_content: IngestedContent) -> ExternalAnalysisResult:
            attempts["openrouter"] += 1
            return ExternalAnalysisResult(
                category=Category.productive,
                confidence=0.9,
                rationale="OpenRouter recovered the request.",
                suggested_reply="Olá! Vamos seguir com a análise.",
                keywords=["schema", "fallback"],
                provider="openrouter:google/gemini-2.0-flash-001",
            )

    monkeypatch.setattr(analysis_module.time, "sleep", lambda _seconds: None)

    result = analyze_ingested_content(
        SAMPLE_CONTENT,
        settings=_settings_stub(
            gemini_api_key="test-gemini-key",
            openrouter_api_key="test-openrouter-key",
        ),
        gemini_provider_factory=InvalidGeminiProvider,
        openrouter_provider_factory=SuccessfulOpenRouterProvider,
    )

    assert attempts["gemini"] == 1
    assert attempts["openrouter"] == 1
    assert result.provider == "openrouter:google/gemini-2.0-flash-001"


def test_circuit_breaker_opens_after_three_failures_and_skips_provider(monkeypatch) -> None:
    attempts = {"gemini": 0, "openrouter": 0}

    class FailingGeminiProvider:
        def __init__(self, *, api_key: str, model: str, timeout_seconds: float) -> None:
            self.api_key = api_key
            self.model = model
            self.timeout_seconds = timeout_seconds

        def analyze(self, ingested_content: IngestedContent) -> ExternalAnalysisResult:
            attempts["gemini"] += 1
            raise ExternalTransportError("timeout")

    class SuccessfulOpenRouterProvider:
        def __init__(self, *, api_key: str, model: str, timeout_seconds: float) -> None:
            self.api_key = api_key
            self.model = model
            self.timeout_seconds = timeout_seconds

        def analyze(self, ingested_content: IngestedContent) -> ExternalAnalysisResult:
            attempts["openrouter"] += 1
            return ExternalAnalysisResult(
                category=Category.productive,
                confidence=0.9,
                rationale="OpenRouter recovered the request.",
                suggested_reply="Olá! Vamos seguir com a análise.",
                keywords=["circuit", "fallback"],
                provider="openrouter:google/gemini-2.0-flash-001",
            )

    monkeypatch.setattr(analysis_module.time, "sleep", lambda _seconds: None)

    settings = _settings_stub(
        gemini_api_key="test-gemini-key",
        openrouter_api_key="test-openrouter-key",
        provider_retry_attempts=0,
    )
    for _ in range(3):
        analyze_ingested_content(
            SAMPLE_CONTENT,
            settings=settings,
            gemini_provider_factory=FailingGeminiProvider,
            openrouter_provider_factory=SuccessfulOpenRouterProvider,
        )

    state = provider_circuit_breakers.snapshot()
    assert state["gemini"].state == "open"

    analyze_ingested_content(
        SAMPLE_CONTENT,
        settings=settings,
        gemini_provider_factory=FailingGeminiProvider,
        openrouter_provider_factory=SuccessfulOpenRouterProvider,
    )

    assert attempts["gemini"] == 3
    assert attempts["openrouter"] == 4
    metrics = operational_metrics.snapshot(circuit_breakers=provider_circuit_breakers.snapshot())
    assert metrics["providers"]["circuit_open_skips"]["gemini"] == 1


def test_analyze_ingested_content_with_trace_records_provider_attempts() -> None:
    class FailingGeminiProvider:
        def __init__(self, *, api_key: str, model: str, timeout_seconds: float) -> None:
            self.api_key = api_key
            self.model = model
            self.timeout_seconds = timeout_seconds

        def analyze(self, ingested_content: IngestedContent) -> ExternalAnalysisResult:
            raise ExternalTransportError("timeout")

    class SuccessfulOpenRouterProvider:
        def __init__(self, *, api_key: str, model: str, timeout_seconds: float) -> None:
            self.api_key = api_key
            self.model = model
            self.timeout_seconds = timeout_seconds

        def analyze(self, ingested_content: IngestedContent) -> ExternalAnalysisResult:
            return ExternalAnalysisResult(
                category=Category.productive,
                confidence=0.9,
                rationale="OpenRouter recovered the request.",
                suggested_reply="Olá! Vamos seguir com a análise.",
                keywords=["request", "fallback"],
                provider="openrouter:google/gemini-2.0-flash-001",
            )

    result, trace = analyze_ingested_content_with_trace(
        SAMPLE_CONTENT,
        settings=_settings_stub(
            gemini_api_key="test-gemini-key",
            openrouter_api_key="test-openrouter-key",
            provider_retry_attempts=0,
        ),
        gemini_provider_factory=FailingGeminiProvider,
        openrouter_provider_factory=SuccessfulOpenRouterProvider,
        request_id="trace-test",
    )

    assert result.provider == "openrouter:google/gemini-2.0-flash-001"
    assert list(trace.provider_attempts) == [
        {"provider": "gemini", "status": "transport"},
        {"provider": "openrouter:google/gemini-2.0-flash-001", "status": "success"},
    ]


def test_analyze_ingested_content_with_trace_marks_missing_provider_keys() -> None:
    result, trace = analyze_ingested_content_with_trace(
        SAMPLE_CONTENT,
        settings=_settings_stub(),
    )

    assert result.provider == FALLBACK_PROVIDER_NO_PROVIDER_KEY
    assert list(trace.provider_attempts) == [
        {"provider": "gemini", "status": "skipped_no_key"},
        {"provider": "openrouter", "status": "skipped_no_key"},
    ]
