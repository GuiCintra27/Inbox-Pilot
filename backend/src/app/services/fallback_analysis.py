from __future__ import annotations

import re
from collections import Counter

from app.core.nlp import stem_token
from app.domain.analysis import AnalysisResult
from app.domain.ingestion import IngestedContent
from app.schemas import Category

FALLBACK_PROVIDER_NO_PROVIDER_KEY = "fallback:no-provider-key"
FALLBACK_PROVIDER_PROVIDER_ERROR = "fallback:provider-error"
FALLBACK_PROVIDER_INVALID_RESPONSE = "fallback:invalid-response"

TEXTUAL_POSITIVE_MARKERS = {
    "follow up": 2,
    "next step": 2,
    "por favor": 1,
    "poderiam": 2,
    "conseguem": 2,
    "please confirm": 2,
    "fico no aguardo": 1,
}

TEXTUAL_NEGATIVE_MARKERS = {
    "thank you": 2,
    "feliz natal": 3,
    "boas festas": 3,
    "happy holidays": 3,
    "merry christmas": 3,
}

_POSITIVE_MARKERS_BY_LANGUAGE = {
    "pt-BR": {
        "aprovação": 2,
        "aprovado": 2,
        "status": 2,
        "atualização": 2,
        "pendência": 2,
        "anexo": 2,
        "arquivo": 1,
        "solicitação": 2,
        "ajuda": 2,
        "suporte": 2,
        "ticket": 2,
        "erro": 2,
        "confirmação": 2,
        "prazo": 1,
        "revisão": 1,
        "pagamento": 2,
        "fornecedor": 1,
        "chamado": 2,
        "resposta": 1,
        "retorno": 1,
        "documento": 1,
        "pedido": 2,
        "cliente": 1,
        "operacional": 1,
    },
    "en-US": {
        "approve": 2,
        "approved": 2,
        "status": 2,
        "update": 2,
        "pending": 2,
        "attachment": 2,
        "file": 1,
        "request": 2,
        "help": 2,
        "support": 2,
        "issue": 2,
        "ticket": 2,
        "error": 2,
        "confirm": 2,
        "deadline": 1,
        "review": 1,
        "payment": 2,
        "supplier": 1,
        "reply": 1,
        "return": 1,
        "document": 1,
        "invoice": 1,
        "customer": 1,
        "operational": 1,
    },
}

_NEGATIVE_MARKERS_BY_LANGUAGE = {
    "pt-BR": {
        "obrigado": 2,
        "agradecimento": 2,
        "felicitação": 2,
        "parabéns": 2,
        "newsletter": 3,
        "convite": 2,
    },
    "en-US": {
        "thanks": 2,
        "gratitude": 2,
        "congratulations": 2,
        "newsletter": 3,
        "invite": 2,
        "greeting": 2,
    },
}


def analyze_with_fallback(
    *,
    ingested_content: IngestedContent,
    provider: str,
) -> AnalysisResult:
    lowered = ingested_content.text.lower()
    stem_counts = Counter(ingested_content.nlp.stems)

    positive_score = 0
    negative_score = 0
    matched_positive: list[str] = []
    matched_negative: list[str] = []

    for marker, score in TEXTUAL_POSITIVE_MARKERS.items():
        if marker in lowered:
            positive_score += score
            matched_positive.append(marker)

    for marker, score in TEXTUAL_NEGATIVE_MARKERS.items():
        if marker in lowered:
            negative_score += score
            matched_negative.append(marker)

    language = (
        ingested_content.nlp.language
        if ingested_content.nlp.language != "unknown"
        else ingested_content.language
    )
    positive_score += _score_stem_markers(
        language=language,
        stem_counts=stem_counts,
        markers=_POSITIVE_MARKERS_BY_LANGUAGE,
        matched=matched_positive,
    )
    negative_score += _score_stem_markers(
        language=language,
        stem_counts=stem_counts,
        markers=_NEGATIVE_MARKERS_BY_LANGUAGE,
        matched=matched_negative,
    )

    if "?" in ingested_content.text:
        positive_score += 1

    token_budget = len(ingested_content.nlp.filtered_tokens) or len(ingested_content.text.split())
    if token_budget < 8 and positive_score == 0:
        negative_score += 1

    if positive_score >= negative_score:
        category = Category.productive
        confidence = min(0.95, 0.62 + 0.06 * (positive_score - negative_score + 1))
        rationale = "A mensagem indica pedido de ação, atualização ou encaminhamento operacional."
        if matched_positive:
            rationale = f"{rationale} Marcadores: {', '.join(sorted(set(matched_positive)))}."
        return AnalysisResult(
            category=category,
            confidence=round(confidence, 2),
            rationale=rationale,
            suggested_reply=_build_reply(
                category=category,
                language=ingested_content.language,
                source=ingested_content.source,
            ),
            keywords=_build_keywords(ingested_content, matched_positive),
            provider=provider,
        )

    category = Category.unproductive
    confidence = min(0.95, 0.62 + 0.06 * (negative_score - positive_score + 1))
    rationale = "A mensagem tem caráter social/informativo e não exige ação imediata."
    if matched_negative:
        rationale = f"{rationale} Marcadores: {', '.join(sorted(set(matched_negative)))}."
    return AnalysisResult(
        category=category,
        confidence=round(confidence, 2),
        rationale=rationale,
        suggested_reply=_build_reply(
            category=category,
            language=ingested_content.language,
            source=ingested_content.source,
        ),
        keywords=_build_keywords(ingested_content, matched_negative),
        provider=provider,
    )


def _build_keywords(ingested_content: IngestedContent, markers: list[str]) -> list[str]:
    tokens = (
        list(ingested_content.nlp.filtered_tokens)
        if ingested_content.nlp.filtered_tokens
        else re.findall(r"[a-zA-ZÀ-ÿ0-9_/-]{3,}", ingested_content.text.lower())
    )
    counts = Counter(tokens)
    keywords = [marker for marker in dict.fromkeys(markers) if marker]
    for token, _count in counts.most_common():
        if token not in keywords:
            keywords.append(token)
        if len(keywords) >= 5:
            break
    return keywords[:5]


def _score_stem_markers(
    *,
    language: str,
    stem_counts: Counter[str],
    markers: dict[str, dict[str, int]],
    matched: list[str],
) -> int:
    resolved_markers = markers.get(language, {})
    score = 0
    for term, weight in resolved_markers.items():
        stem = stem_token(term, language=language)
        if stem_counts.get(stem, 0):
            score += weight
            matched.append(term)
    return score


def _build_reply(*, category: Category, language: str, source: str) -> str:
    if language == "en-US":
        if category == Category.productive:
            return (
                "Hello, thank you for your email. We received your request and will review it "
                "as soon as possible."
            )
        return "Hello, thank you for your message. We appreciate the note and have it on record."

    if category == Category.productive:
        if source == "pdf_file":
            return (
                "Olá! Recebemos o material enviado e vamos revisar o conteúdo para retornar com "
                "uma atualização assim que possível."
            )
        return (
            "Olá! Recebemos sua solicitação e vamos analisar o caso para retornar com os "
            "próximos passos."
        )

    return "Olá! Obrigado pela mensagem. Registramos o contato e agradecemos o envio."
