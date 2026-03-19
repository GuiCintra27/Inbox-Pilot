from __future__ import annotations

import re
from collections import Counter
from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.schemas import AnalyzeResponse, Category
from app.services import (
    EmptyInputError,
    FileDecodingError,
    IngestionError,
    UnsupportedFileTypeError,
    ingest_email_content,
)

router = APIRouter(prefix="")

PROVIDER_NAME = "rule-based-preview"

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

ENGLISH_MARKERS = {
    "hello",
    "thanks",
    "thank you",
    "update",
    "status",
    "attached",
    "attachment",
    "request",
    "support",
    "issue",
    "ticket",
    "deadline",
    "please",
}

PORTUGUESE_MARKERS = {
    "olá",
    "obrigado",
    "atualização",
    "anexo",
    "pedido",
    "solicitação",
    "suporte",
    "ajuda",
    "pendência",
    "prazo",
    "favor",
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


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "inbox-pilot-backend"}


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_email(
    email_text: Annotated[str | None, Form()] = None,
    email_file: Annotated[UploadFile | None, File()] = None,
) -> AnalyzeResponse:
    try:
        file_content = None
        file_name = None
        if email_file is not None:
            file_name = email_file.filename
            file_content = await email_file.read()
            if not file_content:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="O arquivo enviado está vazio.",
                )

        ingested_content = ingest_email_content(
            email_text=email_text,
            email_file_name=file_name,
            email_file_content=file_content,
        )
    except HTTPException:
        raise
    except (EmptyInputError, UnsupportedFileTypeError, FileDecodingError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except IngestionError as exc:  # pragma: no cover - defensive guard
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    category, confidence, rationale, keywords, suggested_reply = _classify_email(
        normalized_text=ingested_content.text,
        language=ingested_content.language,
        source=ingested_content.source,
    )

    return AnalyzeResponse(
        category=category,
        confidence=confidence,
        rationale=rationale,
        suggested_reply=suggested_reply,
        keywords=keywords,
        provider=PROVIDER_NAME,
    )


def _classify_email(
    *,
    normalized_text: str,
    language: str,
    source: str,
) -> tuple[Category, float, str, list[str], str]:
    lowered = normalized_text.lower()

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

    if "?" in normalized_text:
        positive_score += 1

    if len(normalized_text.split()) < 8 and positive_score == 0:
        negative_score += 1

    if positive_score >= negative_score:
        category = Category.productive
        confidence = min(0.95, 0.62 + 0.06 * (positive_score - negative_score + 1))
        rationale = "A mensagem indica pedido de ação, atualização ou encaminhamento operacional."
        if matched_positive:
            rationale = f"{rationale} Marcadores: {', '.join(sorted(set(matched_positive)))}."
        suggested_reply = _build_reply(category=category, language=language, source=source)
        keywords = _build_keywords(normalized_text, matched_positive)
        return category, round(confidence, 2), rationale, keywords, suggested_reply

    category = Category.unproductive
    confidence = min(0.95, 0.62 + 0.06 * (negative_score - positive_score + 1))
    rationale = "A mensagem tem caráter social/informativo e não exige ação imediata."
    if matched_negative:
        rationale = f"{rationale} Marcadores: {', '.join(sorted(set(matched_negative)))}."
    suggested_reply = _build_reply(category=category, language=language, source=source)
    keywords = _build_keywords(normalized_text, matched_negative)
    return category, round(confidence, 2), rationale, keywords, suggested_reply


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
