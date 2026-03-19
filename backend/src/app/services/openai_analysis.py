from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable
from urllib import error, request

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from app.domain.analysis import AnalysisResult
from app.domain.ingestion import IngestedContent
from app.schemas import Category

OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"


class OpenAIProviderError(RuntimeError):
    """Base error for OpenAI provider failures."""


class OpenAIProviderUnavailableError(OpenAIProviderError):
    """Raised when the provider is not configured or cannot be used."""


class OpenAIResponseValidationError(OpenAIProviderError):
    """Raised when the OpenAI response cannot be validated."""


class OpenAITransportError(OpenAIProviderError):
    """Raised when the provider transport fails."""


class OpenAIAnalysisPayload(BaseModel):
    model_config = ConfigDict(extra="ignore")

    category: Category
    confidence: float = Field(ge=0.0, le=1.0)
    rationale: str = Field(min_length=1)
    suggested_reply: str = Field(min_length=1)
    keywords: list[str] = Field(min_length=1, max_length=5)

    @field_validator("category", mode="before")
    @classmethod
    def _normalize_category(cls, value: Any) -> Category:
        if isinstance(value, Category):
            return value
        if not isinstance(value, str):
            raise ValueError("category must be a string")

        normalized = value.strip().lower()
        mapping = {
            "produtivo": Category.productive,
            "productive": Category.productive,
            "improdutivo": Category.unproductive,
            "unproductive": Category.unproductive,
        }
        if normalized not in mapping:
            raise ValueError("category must be Produtivo or Improdutivo")
        return mapping[normalized]

    @field_validator("keywords", mode="before")
    @classmethod
    def _normalize_keywords(cls, value: Any) -> list[str]:
        if isinstance(value, str):
            value = [value]
        if not isinstance(value, list):
            raise ValueError("keywords must be a list of strings")

        normalized_keywords: list[str] = []
        for keyword in value:
            if not isinstance(keyword, str):
                raise ValueError("keywords must contain only strings")
            cleaned = keyword.strip()
            if cleaned and cleaned not in normalized_keywords:
                normalized_keywords.append(cleaned)

        if not normalized_keywords:
            raise ValueError("keywords must not be empty")
        return normalized_keywords[:5]

    @field_validator("rationale", "suggested_reply", mode="before")
    @classmethod
    def _normalize_text_fields(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise ValueError("field must be a string")
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("field must not be empty")
        return cleaned


OpenAIAnalysisResult = AnalysisResult


TransportCallable = Callable[[dict[str, Any]], dict[str, Any]]


@dataclass(slots=True)
class OpenAIAnalysisProvider:
    api_key: str
    model: str
    timeout_seconds: float = 30.0
    transport: TransportCallable | None = None

    def analyze(self, ingested_content: IngestedContent) -> OpenAIAnalysisResult:
        if not self.api_key.strip():
            raise OpenAIProviderUnavailableError("OPENAI_API_KEY não configurada.")

        request_payload = self._build_request_payload(ingested_content)
        response_payload = self._send_request(request_payload)
        return self._parse_response(response_payload)

    def _build_request_payload(self, ingested_content: IngestedContent) -> dict[str, Any]:
        system_prompt = (
            "Você classifica emails operacionais e sugere uma resposta curta e útil. "
            "Retorne apenas um objeto JSON válido com as chaves category, confidence, "
            "rationale, suggested_reply e keywords. category deve ser exatamente "
            '"Produtivo" ou "Improdutivo". confidence deve ficar entre 0 e 1. '
            "keywords deve ser uma lista curta de até 5 termos relevantes."
        )
        user_prompt = (
            f"Linguagem detectada: {ingested_content.language} "
            f"(confiança {ingested_content.language_confidence}).\n"
            f"Origem da entrada: {ingested_content.source}.\n"
            "Analise o conteúdo abaixo e devolva o JSON solicitado.\n\n"
            f"CONTEÚDO:\n{ingested_content.text}"
        )

        return {
            "model": self.model,
            "temperature": 0,
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": (
                        "Linguagem detectada: pt-BR (confiança 0.98).\n"
                        "Origem da entrada: text.\n"
                        "Analise o conteúdo abaixo e devolva o JSON solicitado.\n\n"
                        "CONTEÚDO:\n"
                        "Olá, podem revisar a solicitação em anexo e confirmar o prazo de "
                        "retorno ainda hoje?"
                    ),
                },
                {
                    "role": "assistant",
                    "content": json.dumps(
                        {
                            "category": "Produtivo",
                            "confidence": 0.92,
                            "rationale": "O email pede revisão e confirmação de prazo.",
                            "suggested_reply": (
                                "Olá! Recebemos sua solicitação e vamos revisar o material "
                                "para retornar com uma atualização em breve."
                            ),
                            "keywords": ["solicitação", "anexo", "prazo"],
                        },
                        ensure_ascii=False,
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Linguagem detectada: en-US (confiança 0.94).\n"
                        "Origem da entrada: text.\n"
                        "Analise o conteúdo abaixo e devolva o JSON solicitado.\n\n"
                        "CONTEÚDO:\n"
                        "Thanks for the warm welcome and congratulations to the whole team."
                    ),
                },
                {
                    "role": "assistant",
                    "content": json.dumps(
                        {
                            "category": "Improdutivo",
                            "confidence": 0.88,
                            "rationale": "The message is social and does not request action.",
                            "suggested_reply": (
                                "Hello! Thank you for your message. We appreciate the note "
                                "and have it on record."
                            ),
                            "keywords": ["thanks", "welcome", "team"],
                        }
                    ),
                },
                {"role": "user", "content": user_prompt},
            ],
            "response_format": {"type": "json_object"},
        }

    def _send_request(self, request_payload: dict[str, Any]) -> dict[str, Any]:
        if self.transport is not None:
            return self.transport(request_payload)

        body = json.dumps(request_payload).encode("utf-8")
        http_request = request.Request(
            url=OPENAI_CHAT_COMPLETIONS_URL,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )

        try:
            with request.urlopen(http_request, timeout=self.timeout_seconds) as response:
                raw_response = response.read().decode("utf-8")
        except error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
            raise OpenAITransportError(
                f"OpenAI retornou HTTP {exc.code}: {error_body[:500]}"
            ) from exc
        except error.URLError as exc:
            raise OpenAITransportError("Falha de transporte ao chamar OpenAI.") from exc
        except TimeoutError as exc:  # pragma: no cover - defensive guard
            raise OpenAITransportError("Timeout ao chamar OpenAI.") from exc

        try:
            return json.loads(raw_response)
        except json.JSONDecodeError as exc:
            raise OpenAITransportError("Resposta da OpenAI não é um JSON válido.") from exc

    def _parse_response(self, response_payload: dict[str, Any]) -> OpenAIAnalysisResult:
        content = self._extract_message_content(response_payload)

        try:
            parsed_content = json.loads(content)
        except json.JSONDecodeError as exc:
            raise OpenAIResponseValidationError(
                "A resposta da OpenAI não contém um objeto JSON válido."
            ) from exc

        try:
            validated_payload = OpenAIAnalysisPayload.model_validate(parsed_content)
        except ValidationError as exc:
            raise OpenAIResponseValidationError(
                "A resposta da OpenAI não corresponde ao esquema esperado."
            ) from exc

        return OpenAIAnalysisResult(
            category=validated_payload.category,
            confidence=round(validated_payload.confidence, 2),
            rationale=validated_payload.rationale,
            suggested_reply=validated_payload.suggested_reply,
            keywords=validated_payload.keywords,
            provider=f"openai:{self.model}",
        )

    @staticmethod
    def _extract_message_content(response_payload: dict[str, Any]) -> str:
        choices = response_payload.get("choices")
        if not isinstance(choices, list) or not choices:
            raise OpenAIResponseValidationError(
                "A resposta da OpenAI não contém escolhas válidas."
            )

        message = choices[0].get("message")
        if not isinstance(message, dict):
            raise OpenAIResponseValidationError(
                "A resposta da OpenAI não contém a mensagem esperada."
            )

        content = message.get("content")
        if not isinstance(content, str) or not content.strip():
            raise OpenAIResponseValidationError(
                "A resposta da OpenAI não contém conteúdo textual válido."
            )

        return content
