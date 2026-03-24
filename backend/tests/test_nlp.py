from __future__ import annotations

from app.core.nlp import build_nlp_artifacts
from app.domain.ingestion import IngestedContent
from app.services.fallback_analysis import analyze_with_fallback


def test_build_nlp_artifacts_removes_stopwords_and_generates_stems() -> None:
    artifacts = build_nlp_artifacts(
        "As solicitações aprovadas seguem pendentes para revisão do fornecedor.",
        language="pt-BR",
    )

    assert "as" in artifacts.tokens
    assert "as" not in artifacts.filtered_tokens
    assert "solicitações" in artifacts.filtered_tokens
    assert "aprov" in artifacts.stems
    assert artifacts.stopwords_removed >= 1
    assert artifacts.processed_text


def test_build_nlp_artifacts_supports_english_stemming() -> None:
    artifacts = build_nlp_artifacts(
        "The requests were approved and the responses are pending review.",
        language="en-US",
    )

    assert "the" in artifacts.tokens
    assert "the" not in artifacts.filtered_tokens
    assert "approv" in artifacts.stems
    assert "respons" in artifacts.stems


def test_fallback_uses_nlp_stems_for_plural_operational_requests() -> None:
    sample_text = (
        "As solicitações aprovadas e as pendências documentais seguem abertas "
        "e precisam de atualizações para os fornecedores."
    )
    ingested_content = IngestedContent(
        text=sample_text,
        source="text",
        language="pt-BR",
        language_confidence=0.92,
        nlp=build_nlp_artifacts(sample_text, language="pt-BR"),
    )

    result = analyze_with_fallback(
        ingested_content=ingested_content,
        provider="fallback:no-provider-key",
    )

    assert result.category.value == "Produtivo"
    assert any(
        keyword in result.keywords for keyword in ["solicitação", "aprovação", "pendência"]
    )

