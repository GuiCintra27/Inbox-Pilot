from __future__ import annotations

import time
from dataclasses import dataclass, replace
from typing import Any

from app.core.config import Settings, get_settings
from app.core.redaction import RedactionResult, redact_provider_input
from app.core.security import (
    derive_fallback_reason,
    log_analysis_event,
    operational_metrics,
    provider_circuit_breakers,
)
from app.domain.analysis import AnalysisResult
from app.domain.ingestion import IngestedContent
from app.services.fallback_analysis import (
    FALLBACK_PROVIDER_INVALID_RESPONSE,
    FALLBACK_PROVIDER_NO_PROVIDER_KEY,
    FALLBACK_PROVIDER_PROVIDER_ERROR,
    analyze_with_fallback,
)
from app.services.llm_analysis import (
    ExternalProviderError,
    ExternalResponseValidationError,
    ExternalTransportError,
    GeminiAnalysisProvider,
    OpenRouterAnalysisProvider,
)


@dataclass(frozen=True, slots=True)
class AnalysisAuditTrace:
    provider_attempts: tuple[dict[str, object], ...]
    redaction_summary: dict[str, int]
    final_provider: str
    fallback_reason: str | None


def analyze_ingested_content(
    ingested_content: IngestedContent,
    *,
    settings: Settings | None = None,
    gemini_provider_factory: type[GeminiAnalysisProvider] = GeminiAnalysisProvider,
    openrouter_provider_factory: type[OpenRouterAnalysisProvider] = OpenRouterAnalysisProvider,
    request_id: str | None = None,
) -> AnalysisResult:
    result, _ = analyze_ingested_content_with_trace(
        ingested_content,
        settings=settings,
        gemini_provider_factory=gemini_provider_factory,
        openrouter_provider_factory=openrouter_provider_factory,
        request_id=request_id,
    )
    return result


def analyze_ingested_content_with_trace(
    ingested_content: IngestedContent,
    *,
    settings: Settings | None = None,
    gemini_provider_factory: type[GeminiAnalysisProvider] = GeminiAnalysisProvider,
    openrouter_provider_factory: type[OpenRouterAnalysisProvider] = OpenRouterAnalysisProvider,
    request_id: str | None = None,
) -> tuple[AnalysisResult, AnalysisAuditTrace]:
    resolved_settings = settings or get_settings()
    provider_configured = False
    saw_validation_error = False
    provider_attempts: list[dict[str, object]] = []

    provider_input, redaction_result = _prepare_provider_input(
        ingested_content,
        settings=resolved_settings,
    )

    if (
        resolved_settings.gemini_api_key.strip() or resolved_settings.openrouter_api_key.strip()
    ) and redaction_result.counts:
        operational_metrics.record_redactions(redaction_result.counts)

    if resolved_settings.gemini_api_key.strip():
        provider_configured = True
        result, validation_failed = _attempt_provider(
            provider_name="gemini",
            provider_factory=gemini_provider_factory,
            api_key=resolved_settings.gemini_api_key,
            model=resolved_settings.gemini_model,
            ingested_content=provider_input,
            settings=resolved_settings,
            provider_attempts=provider_attempts,
            request_id=request_id,
        )
        if result is not None:
            _record_provider_success(result.provider)
            return result, _build_trace(
                provider_attempts=provider_attempts,
                redaction_result=redaction_result,
                final_provider=result.provider,
            )
        saw_validation_error = saw_validation_error or validation_failed
    else:
        provider_attempts.append({"provider": "gemini", "status": "skipped_no_key"})

    if resolved_settings.openrouter_api_key.strip():
        provider_configured = True
        result, validation_failed = _attempt_provider(
            provider_name="openrouter",
            provider_factory=openrouter_provider_factory,
            api_key=resolved_settings.openrouter_api_key,
            model=resolved_settings.openrouter_model,
            ingested_content=provider_input,
            settings=resolved_settings,
            provider_attempts=provider_attempts,
            request_id=request_id,
        )
        if result is not None:
            _record_provider_success(result.provider)
            return result, _build_trace(
                provider_attempts=provider_attempts,
                redaction_result=redaction_result,
                final_provider=result.provider,
            )
        saw_validation_error = saw_validation_error or validation_failed
    else:
        provider_attempts.append({"provider": "openrouter", "status": "skipped_no_key"})

    if not provider_configured:
        operational_metrics.record_fallback("no-provider-key")
        result = analyze_with_fallback(
            ingested_content=ingested_content,
            provider=FALLBACK_PROVIDER_NO_PROVIDER_KEY,
        )
        return result, _build_trace(
            provider_attempts=provider_attempts,
            redaction_result=redaction_result,
            final_provider=result.provider,
        )

    fallback_provider = (
        FALLBACK_PROVIDER_INVALID_RESPONSE
        if saw_validation_error
        else FALLBACK_PROVIDER_PROVIDER_ERROR
    )
    fallback_reason = derive_fallback_reason(fallback_provider) or "provider-error"
    operational_metrics.record_fallback(fallback_reason)
    result = analyze_with_fallback(
        ingested_content=ingested_content,
        provider=fallback_provider,
    )
    return result, _build_trace(
        provider_attempts=provider_attempts,
        redaction_result=redaction_result,
        final_provider=result.provider,
    )


def _prepare_provider_input(
    ingested_content: IngestedContent,
    *,
    settings: Settings,
) -> tuple[IngestedContent, RedactionResult]:
    redaction_result = redact_provider_input(
        ingested_content.text,
        enabled=settings.redaction_enabled,
    )
    provider_input = replace(ingested_content, text=redaction_result.text)
    provider_input = _truncate_for_provider(
        provider_input,
        max_chars=settings.max_provider_input_chars,
    )
    return provider_input, redaction_result


def _attempt_provider(
    *,
    provider_name: str,
    provider_factory: type[Any],
    api_key: str,
    model: str,
    ingested_content: IngestedContent,
    settings: Settings,
    provider_attempts: list[dict[str, object]],
    request_id: str | None,
) -> tuple[AnalysisResult | None, bool]:
    if provider_circuit_breakers.is_open(provider_name):
        provider_attempts.append({"provider": provider_name, "status": "circuit_open"})
        operational_metrics.record_provider_circuit_open(provider_name)
        log_analysis_event(
            event_name="provider_circuit_open",
            request_id=request_id,
            provider=provider_name,
            state="open",
        )
        return None, False

    provider = _build_provider(
        provider_factory=provider_factory,
        api_key=api_key,
        model=model,
        timeout_seconds=settings.provider_timeout_seconds,
    )

    attempts = settings.provider_retry_attempts + 1
    for attempt_index in range(1, attempts + 1):
        try:
            result = provider.analyze(ingested_content)
        except ExternalTransportError as exc:
            provider_attempts.append({"provider": provider_name, "status": "transport"})
            operational_metrics.record_provider_transport_error(provider_name)
            opened = provider_circuit_breakers.record_failure(
                provider_name,
                threshold=settings.circuit_breaker_failure_threshold,
                open_seconds=settings.circuit_breaker_open_seconds,
            )
            log_analysis_event(
                event_name="provider_transport_error",
                request_id=request_id,
                provider=provider_name,
                attempt=attempt_index,
                opened_circuit=opened,
                detail=str(exc),
            )
            if opened:
                return None, False
            if attempt_index < attempts:
                time.sleep(settings.provider_retry_backoff_ms / 1000)
                continue
            return None, False
        except ExternalResponseValidationError as exc:
            provider_attempts.append({"provider": provider_name, "status": "schema"})
            operational_metrics.record_provider_schema_error(provider_name)
            opened = provider_circuit_breakers.record_failure(
                provider_name,
                threshold=settings.circuit_breaker_failure_threshold,
                open_seconds=settings.circuit_breaker_open_seconds,
            )
            log_analysis_event(
                event_name="provider_schema_error",
                request_id=request_id,
                provider=provider_name,
                attempt=attempt_index,
                opened_circuit=opened,
                detail=str(exc),
            )
            return None, True
        except ExternalProviderError as exc:
            provider_attempts.append(
                {
                    "provider": provider_name,
                    "status": "transport",
                    "reason": "provider_error",
                }
            )
            operational_metrics.record_provider_generic_error(provider_name)
            opened = provider_circuit_breakers.record_failure(
                provider_name,
                threshold=settings.circuit_breaker_failure_threshold,
                open_seconds=settings.circuit_breaker_open_seconds,
            )
            log_analysis_event(
                event_name="provider_error",
                request_id=request_id,
                provider=provider_name,
                attempt=attempt_index,
                opened_circuit=opened,
                detail=str(exc),
            )
            return None, False
        else:
            provider_attempts.append({"provider": result.provider, "status": "success"})
            provider_circuit_breakers.record_success(provider_name)
            return result, False

    return None, False


def _build_provider(
    *,
    provider_factory: type[Any],
    api_key: str,
    model: str,
    timeout_seconds: float,
) -> Any:
    try:
        return provider_factory(
            api_key=api_key,
            model=model,
            timeout_seconds=timeout_seconds,
        )
    except TypeError:
        return provider_factory(api_key=api_key, model=model)


def _record_provider_success(provider_label: str) -> None:
    provider_name = provider_label.split(":", maxsplit=1)[0]
    operational_metrics.record_provider_success(provider_name)


def _truncate_for_provider(ingested_content: IngestedContent, *, max_chars: int) -> IngestedContent:
    if len(ingested_content.text) <= max_chars:
        return ingested_content

    truncated_text = ingested_content.text[:max_chars].rstrip()
    return replace(ingested_content, text=truncated_text)


def _build_trace(
    *,
    provider_attempts: list[dict[str, object]],
    redaction_result: RedactionResult,
    final_provider: str,
) -> AnalysisAuditTrace:
    return AnalysisAuditTrace(
        provider_attempts=tuple(provider_attempts),
        redaction_summary=dict(redaction_result.counts),
        final_provider=final_provider,
        fallback_reason=derive_fallback_reason(final_provider),
    )
