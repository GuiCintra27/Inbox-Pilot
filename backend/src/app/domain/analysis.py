from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from app.schemas import Category


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    category: Category
    confidence: float
    rationale: str
    suggested_reply: str
    keywords: list[str]
    provider: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
