from __future__ import annotations

import re

_ZERO_WIDTH_CHARS = ("\u200b", "\u200c", "\u200d", "\ufeff")
_WHITESPACE_RE = re.compile(r"[ \t\f\v]+")
_BLANK_LINES_RE = re.compile(r"\n{3,}")
_INLINE_SPACES_RE = re.compile(r" *\n *")
_TOKEN_RE = re.compile(r"[A-Za-zÀ-ÿ0-9']+")


def strip_control_characters(text: str) -> str:
    cleaned = text.replace("\r\n", "\n").replace("\r", "\n")
    cleaned = cleaned.replace("\x0c", "\n\n")
    for character in _ZERO_WIDTH_CHARS:
        cleaned = cleaned.replace(character, "")
    return cleaned


def normalize_text(text: str) -> str:
    if not text:
        return ""

    cleaned = strip_control_characters(text)
    cleaned = _WHITESPACE_RE.sub(" ", cleaned)
    cleaned = _INLINE_SPACES_RE.sub("\n", cleaned)
    cleaned = _BLANK_LINES_RE.sub("\n\n", cleaned)
    return cleaned.strip()


def tokenize_text(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())
