from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_RE = re.compile(
    r"(?<!\w)(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,3}\)?[\s.-]?)?\d{4,5}[\s.-]?\d{4}(?!\w)"
)
CPF_RE = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")
CNPJ_RE = re.compile(r"\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b")
OPERATIONAL_ID_RE = re.compile(
    r"(?i)\b("
    r"pedido|order|invoice|fatura|ticket|chamado|protocolo|ref|refer[eê]ncia|nota fiscal"
    r")\b(\s*(?:n[oº.]?|number|num(?:ber)?|#|:|-)?\s*)([A-Z0-9][A-Z0-9._/-]{2,})"
)


@dataclass(frozen=True, slots=True)
class RedactionResult:
    text: str
    counts: dict[str, int]


def redact_provider_input(text: str, *, enabled: bool) -> RedactionResult:
    if not enabled:
        return RedactionResult(text=text, counts={})

    counts: Counter[str] = Counter()
    redacted = text

    redacted = _replace_with_token(redacted, EMAIL_RE, "[EMAIL]", counts, "email")
    redacted = _replace_with_token(redacted, PHONE_RE, "[PHONE]", counts, "phone")
    redacted = _replace_with_token(redacted, CPF_RE, "[CPF]", counts, "cpf")
    redacted = _replace_with_token(redacted, CNPJ_RE, "[CNPJ]", counts, "cnpj")
    redacted = _replace_operational_ids(redacted, counts)

    return RedactionResult(text=redacted, counts=dict(counts))


def _replace_with_token(
    text: str,
    pattern: re.Pattern[str],
    token: str,
    counts: Counter[str],
    counter_key: str,
) -> str:
    def _replacer(match: re.Match[str]) -> str:
        counts[counter_key] += 1
        return token

    return pattern.sub(_replacer, text)


def _replace_operational_ids(text: str, counts: Counter[str]) -> str:
    def _replacer(match: re.Match[str]) -> str:
        counts["op_id"] += 1
        return f"{match.group(1)}{match.group(2)}[OP_ID]"

    return OPERATIONAL_ID_RE.sub(_replacer, text)

