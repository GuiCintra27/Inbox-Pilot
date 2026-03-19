from enum import Enum

from pydantic import BaseModel, Field


class Category(str, Enum):
    productive = "Produtivo"
    unproductive = "Improdutivo"


class AnalyzeResponse(BaseModel):
    category: Category
    confidence: float = Field(ge=0.0, le=1.0)
    rationale: str
    suggested_reply: str
    keywords: list[str]
    provider: str
