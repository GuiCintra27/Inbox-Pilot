from __future__ import annotations

from app.core.config import Settings, get_settings
from app.domain.analysis import AnalysisResult
from app.domain.ingestion import IngestedContent
from app.services.fallback_analysis import (
    FALLBACK_PROVIDER_INVALID_RESPONSE,
    FALLBACK_PROVIDER_NO_OPENAI_KEY,
    FALLBACK_PROVIDER_PROVIDER_ERROR,
    analyze_with_fallback,
)
from app.services.openai_analysis import (
    OpenAIAnalysisProvider,
    OpenAIProviderError,
    OpenAIResponseValidationError,
)


def analyze_ingested_content(
    ingested_content: IngestedContent,
    *,
    settings: Settings | None = None,
    provider_factory: type[OpenAIAnalysisProvider] = OpenAIAnalysisProvider,
) -> AnalysisResult:
    resolved_settings = settings or get_settings()
    if not resolved_settings.openai_api_key.strip():
        return analyze_with_fallback(
            ingested_content=ingested_content,
            provider=FALLBACK_PROVIDER_NO_OPENAI_KEY,
        )

    provider = provider_factory(
        api_key=resolved_settings.openai_api_key,
        model=resolved_settings.openai_model,
    )

    try:
        return provider.analyze(ingested_content)
    except OpenAIResponseValidationError:
        return analyze_with_fallback(
            ingested_content=ingested_content,
            provider=FALLBACK_PROVIDER_INVALID_RESPONSE,
        )
    except OpenAIProviderError:
        return analyze_with_fallback(
            ingested_content=ingested_content,
            provider=FALLBACK_PROVIDER_PROVIDER_ERROR,
        )
