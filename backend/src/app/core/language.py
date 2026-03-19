from __future__ import annotations

from dataclasses import dataclass

from app.core.text import tokenize_text

_PORTUGUESE_MARKERS = {
    "a",
    "ao",
    "aos",
    "da",
    "das",
    "de",
    "deve",
    "email",
    "em",
    "este",
    "esta",
    "ficou",
    "não",
    "para",
    "por",
    "que",
    "se",
    "sou",
    "você",
}
_ENGLISH_MARKERS = {
    "a",
    "about",
    "and",
    "email",
    "for",
    "hello",
    "hi",
    "please",
    "regards",
    "the",
    "thanks",
    "to",
    "you",
}


@dataclass(frozen=True, slots=True)
class LanguageGuess:
    language: str
    confidence: float


def detect_language(text: str) -> LanguageGuess:
    tokens = tokenize_text(text)
    if not tokens:
        return LanguageGuess(language="unknown", confidence=0.0)

    portuguese_score = sum(1 for token in tokens if token in _PORTUGUESE_MARKERS)
    english_score = sum(1 for token in tokens if token in _ENGLISH_MARKERS)
    accent_score = sum(1 for char in text if char in "áàâãéêíóôõúç")

    portuguese_score += accent_score

    if portuguese_score == 0 and english_score == 0:
        return LanguageGuess(language="unknown", confidence=0.0)

    if portuguese_score >= english_score:
        total = portuguese_score + english_score
        confidence = portuguese_score / total if total else 0.5
        return LanguageGuess(language="pt-BR", confidence=round(confidence, 2))

    total = portuguese_score + english_score
    confidence = english_score / total if total else 0.5
    return LanguageGuess(language="en-US", confidence=round(confidence, 2))
