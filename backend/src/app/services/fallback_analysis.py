from __future__ import annotations

import re
from collections import Counter

from app.domain.analysis import AnalysisResult
from app.domain.ingestion import IngestedContent
from app.schemas import Category

FALLBACK_PROVIDER_NO_PROVIDER_KEY = "fallback:no-provider-key"
# Backward-compatible alias for old tests/docs that may still import the older name.
FALLBACK_PROVIDER_NO_OPENAI_KEY = FALLBACK_PROVIDER_NO_PROVIDER_KEY
FALLBACK_PROVIDER_PROVIDER_ERROR = "fallback:provider-error"
FALLBACK_PROVIDER_INVALID_RESPONSE = "fallback:invalid-response"

TEXTUAL_POSITIVE_MARKERS = {
    "approve": 2,
    "approved": 2,
    "status": 2,
    "atualizacao": 2,
    "atualização": 2,
    "pendencia": 2,
    "pendência": 2,
    "anexo": 2,
    "arquivo": 1,
    "solicitacao": 2,
    "solicitação": 2,
    "ajuda": 2,
    "support": 2,
    "issue": 2,
    "ticket": 2,
    "error": 2,
    "erro": 2,
    "confirm": 2,
    "invoice": 1,
    "please": 1,
    "prazo": 1,
    "deadline": 1,
    "today": 1,
    "review": 1,
}

TEXTUAL_NEGATIVE_MARKERS = {
    "obrigado": 2,
    "agradeco": 2,
    "agradeço": 2,
    "thanks": 2,
    "thank you": 2,
    "feliz natal": 3,
    "parabens": 2,
    "parabéns": 2,
    "congratulations": 2,
}

STOPWORDS = {
    "a",
    "ao",
    "aos",
    "as",
    "com",
    "como",
    "da",
    "das",
    "de",
    "do",
    "dos",
    "e",
    "em",
    "entre",
    "essa",
    "esse",
    "esta",
    "este",
    "foi",
    "mas",
    "na",
    "nas",
    "no",
    "nos",
    "o",
    "os",
    "ou",
    "para",
    "por",
    "que",
    "se",
    "sem",
    "sua",
    "suas",
    "seu",
    "seus",
    "uma",
    "um",
    "uns",
    "umas",
    "the",
    "and",
    "or",
    "of",
    "to",
    "for",
    "with",
    "from",
    "your",
    "you",
    "are",
    "is",
}


def analyze_with_fallback(
    *,
    ingested_content: IngestedContent,
    provider: str,
) -> AnalysisResult:
    lowered = ingested_content.text.lower()

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

    if "?" in ingested_content.text:
        positive_score += 1

    if len(ingested_content.text.split()) < 8 and positive_score == 0:
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
            keywords=_build_keywords(ingested_content.text, matched_positive),
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
        keywords=_build_keywords(ingested_content.text, matched_negative),
        provider=provider,
    )


def _build_keywords(text: str, markers: list[str]) -> list[str]:
    tokens = re.findall(r"[a-zA-ZÀ-ÿ0-9_/-]{3,}", text.lower())
    counts = Counter(token for token in tokens if token not in STOPWORDS)
    keywords = [marker for marker in dict.fromkeys(markers) if marker]
    for token, _count in counts.most_common():
        if token not in keywords:
            keywords.append(token)
        if len(keywords) >= 5:
            break
    return keywords[:5]


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
