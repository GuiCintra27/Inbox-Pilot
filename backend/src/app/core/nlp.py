from __future__ import annotations

from functools import lru_cache

from nltk.stem.snowball import SnowballStemmer

from app.core.text import tokenize_text
from app.domain.ingestion import NlpArtifacts

_PORTUGUESE_STOPWORDS = frozenset(
    {
        "a",
        "ao",
        "aos",
        "aquela",
        "aquelas",
        "aquele",
        "aqueles",
        "aquilo",
        "as",
        "até",
        "com",
        "como",
        "da",
        "das",
        "de",
        "dela",
        "dele",
        "deles",
        "depois",
        "do",
        "dos",
        "e",
        "ela",
        "elas",
        "ele",
        "eles",
        "em",
        "entre",
        "era",
        "eram",
        "essa",
        "essas",
        "esse",
        "esses",
        "esta",
        "está",
        "estamos",
        "estão",
        "estar",
        "estas",
        "este",
        "esteja",
        "estejam",
        "estejamos",
        "estes",
        "eu",
        "foi",
        "foram",
        "há",
        "isso",
        "isto",
        "já",
        "lhe",
        "lhes",
        "mais",
        "mas",
        "me",
        "mesmo",
        "meu",
        "meus",
        "minha",
        "minhas",
        "muito",
        "na",
        "não",
        "nas",
        "nem",
        "no",
        "nos",
        "nós",
        "o",
        "os",
        "ou",
        "para",
        "pela",
        "pelas",
        "pelo",
        "pelos",
        "por",
        "porque",
        "que",
        "quem",
        "se",
        "sem",
        "ser",
        "seu",
        "seus",
        "sua",
        "suas",
        "também",
        "te",
        "tem",
        "tendo",
        "tenho",
        "ter",
        "teve",
        "tive",
        "tivemos",
        "todo",
        "todos",
        "uma",
        "umas",
        "um",
        "uns",
        "você",
        "vocês",
    }
)

_ENGLISH_STOPWORDS = frozenset(
    {
        "a",
        "about",
        "after",
        "all",
        "also",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "been",
        "before",
        "being",
        "between",
        "but",
        "by",
        "can",
        "could",
        "did",
        "do",
        "does",
        "for",
        "from",
        "had",
        "has",
        "have",
        "he",
        "her",
        "here",
        "hers",
        "him",
        "his",
        "how",
        "i",
        "if",
        "in",
        "into",
        "is",
        "it",
        "its",
        "just",
        "me",
        "more",
        "most",
        "my",
        "no",
        "not",
        "of",
        "on",
        "or",
        "our",
        "ours",
        "please",
        "she",
        "so",
        "some",
        "than",
        "that",
        "the",
        "their",
        "them",
        "then",
        "there",
        "these",
        "they",
        "this",
        "those",
        "to",
        "us",
        "was",
        "we",
        "were",
        "what",
        "when",
        "where",
        "which",
        "while",
        "who",
        "will",
        "with",
        "would",
        "you",
        "your",
        "yours",
    }
)

_LANGUAGE_TO_STEMMER = {
    "pt-BR": "portuguese",
    "en-US": "english",
}
_LANGUAGE_STOPWORDS = {
    "pt-BR": _PORTUGUESE_STOPWORDS,
    "en-US": _ENGLISH_STOPWORDS,
}
_COMMON_STOPWORDS = _PORTUGUESE_STOPWORDS | _ENGLISH_STOPWORDS


def build_nlp_artifacts(text: str, *, language: str) -> NlpArtifacts:
    tokens = tuple(tokenize_text(text))
    if not tokens:
        return NlpArtifacts.empty(language=language)

    stopwords = _LANGUAGE_STOPWORDS.get(language, _COMMON_STOPWORDS)
    filtered_tokens = tuple(token for token in tokens if _should_keep_token(token, stopwords))
    stems = tuple(_stem_token(token, language=language) for token in filtered_tokens)

    return NlpArtifacts(
        language=language,
        tokens=tokens,
        filtered_tokens=filtered_tokens,
        stems=stems,
        processed_text=" ".join(stems),
        stopwords_removed=max(0, len(tokens) - len(filtered_tokens)),
    )


def stem_token(token: str, *, language: str) -> str:
    return _stem_token(token.lower(), language=language)


def _should_keep_token(token: str, stopwords: frozenset[str]) -> bool:
    if token in stopwords:
        return False
    if token.isdigit():
        return len(token) > 1
    if len(token) <= 2:
        return False
    return any(character.isalpha() for character in token)


def _stem_token(token: str, *, language: str) -> str:
    stemmer = _get_stemmer(language)
    if stemmer is None:
        return token
    return stemmer.stem(token)


@lru_cache(maxsize=4)
def _get_stemmer(language: str) -> SnowballStemmer | None:
    stemmer_language = _LANGUAGE_TO_STEMMER.get(language)
    if stemmer_language is None:
        return None
    return SnowballStemmer(stemmer_language)


__all__ = [
    "build_nlp_artifacts",
    "stem_token",
]
