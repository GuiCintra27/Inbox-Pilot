from __future__ import annotations

from app.core.config import Settings, get_settings
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
    GeminiAnalysisProvider,
    OpenRouterAnalysisProvider,
)


def analyze_ingested_content(
    ingested_content: IngestedContent,
    *,
    settings: Settings | None = None,
    gemini_provider_factory: type[GeminiAnalysisProvider] = GeminiAnalysisProvider,
    openrouter_provider_factory: type[OpenRouterAnalysisProvider] = OpenRouterAnalysisProvider,
) -> AnalysisResult:
    resolved_settings = settings or get_settings()
    provider_attempted = False
    saw_validation_error = False

    if resolved_settings.gemini_api_key.strip():
        provider_attempted = True
        provider = gemini_provider_factory(
            api_key=resolved_settings.gemini_api_key,
            model=resolved_settings.gemini_model,
        )

        try:
            return provider.analyze(ingested_content)
        except ExternalResponseValidationError:
            saw_validation_error = True
        except ExternalProviderError:
            pass

    if resolved_settings.openrouter_api_key.strip():
        provider_attempted = True
        provider = openrouter_provider_factory(
            api_key=resolved_settings.openrouter_api_key,
            model=resolved_settings.openrouter_model,
        )

        try:
            return provider.analyze(ingested_content)
        except ExternalResponseValidationError:
            saw_validation_error = True
        except ExternalProviderError:
            pass

    if not provider_attempted:
        return analyze_with_fallback(
            ingested_content=ingested_content,
            provider=FALLBACK_PROVIDER_NO_PROVIDER_KEY,
        )

    return analyze_with_fallback(
        ingested_content=ingested_content,
        provider=(
            FALLBACK_PROVIDER_INVALID_RESPONSE
            if saw_validation_error
            else FALLBACK_PROVIDER_PROVIDER_ERROR
        ),
    )
