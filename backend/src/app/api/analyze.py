from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, Request, Response, UploadFile, status

from app.core.config import get_settings
from app.core.security import (
    analyze_rate_limiter,
    audit_trail,
    derive_fallback_reason,
    log_analysis_event,
    operational_metrics,
    resolve_request_id,
)
from app.schemas import AnalyzeResponse
from app.services import (
    EmptyInputError,
    FileDecodingError,
    FileTypeMismatchError,
    IngestionError,
    InputTooLargeError,
    PdfPageLimitError,
    UnsupportedFileTypeError,
    analyze_ingested_content_with_trace,
    ingest_email_content,
)

router = APIRouter(prefix="")


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "inbox-pilot-backend"}


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_email(
    request: Request,
    response: Response,
    email_text: Annotated[str | None, Form()] = None,
    email_file: Annotated[UploadFile | None, File()] = None,
) -> AnalyzeResponse:
    started_at = time.perf_counter()
    settings = get_settings()
    request_id = resolve_request_id(request.headers.get(settings.audit_request_id_header))
    operational_metrics.record_request_started()
    client_ip = _extract_client_ip(request)
    rate_limit = analyze_rate_limiter.check(
        client_ip,
        limit=settings.rate_limit_analyze_requests,
        window_seconds=settings.rate_limit_window_seconds,
    )
    if not rate_limit.allowed:
        operational_metrics.record_rate_limit_hit()
        operational_metrics.record_request_outcome("rate_limited")
        headers = {
            "Retry-After": str(rate_limit.retry_after_seconds),
            settings.audit_request_id_header: request_id,
        }
        _record_audit_event(
            settings=settings,
            request_id=request_id,
            source="unknown",
            file_type="none",
            input_chars=0,
            provider_attempts=[],
            final_provider="none",
            status_label="rate_limited",
            started_at=started_at,
            fallback_reason=None,
            redaction_summary={},
        )
        _log_request(
            request_id=request_id,
            source="unknown",
            file_type="none",
            input_chars=0,
            provider="none",
            status_label="rate_limited",
            started_at=started_at,
            fallback_reason=None,
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Muitas solicitações para /analyze. Tente novamente em instantes.",
            headers=headers,
        )

    response.headers[settings.audit_request_id_header] = request_id
    file_type = "none"
    source = "unknown"
    try:
        file_content = None
        file_name = None
        if email_file is not None:
            file_name = email_file.filename
            file_type = _sanitize_file_type(file_name)
            source = f"{file_type}_file" if file_type in {"txt", "pdf"} else "upload"
            file_content = await email_file.read()
            if not file_content:
                _log_request(
                    request_id=request_id,
                    source=source,
                    file_type=file_type,
                    input_chars=0,
                    provider="none",
                    status_label="validation_error",
                    started_at=started_at,
                    fallback_reason=None,
                )
                _raise_http_error(
                    header_name=settings.audit_request_id_header,
                    request_id=request_id,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="O arquivo enviado está vazio.",
                )
            if len(file_content) > settings.max_upload_bytes:
                _log_request(
                    request_id=request_id,
                    source=source,
                    file_type=file_type,
                    input_chars=0,
                    provider="none",
                    status_label="validation_error",
                    started_at=started_at,
                    fallback_reason=None,
                )
                _raise_http_error(
                    header_name=settings.audit_request_id_header,
                    request_id=request_id,
                    status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                    detail="O arquivo enviado excede o limite permitido para análise.",
                )
        elif email_text is not None:
            source = "text"

        ingested_content = ingest_email_content(
            email_text=email_text,
            email_file_name=file_name,
            email_file_content=file_content,
            settings=settings,
        )
    except HTTPException:
        raise
    except EmptyInputError as exc:
        operational_metrics.record_request_outcome("validation_error")
        _log_request(
            request_id=request_id,
            source=source,
            file_type=file_type,
            input_chars=0,
            provider="none",
            status_label="validation_error",
            started_at=started_at,
            fallback_reason=None,
        )
        _record_audit_event(
            settings=settings,
            request_id=request_id,
            source=source,
            file_type=file_type,
            input_chars=0,
            provider_attempts=[],
            final_provider="none",
            status_label="validation_error",
            started_at=started_at,
            fallback_reason=None,
            redaction_summary={},
        )
        _raise_http_error(
            header_name=settings.audit_request_id_header,
            request_id=request_id,
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except (InputTooLargeError, PdfPageLimitError) as exc:
        operational_metrics.record_request_outcome("validation_error")
        _log_request(
            request_id=request_id,
            source=source,
            file_type=file_type,
            input_chars=0,
            provider="none",
            status_label="validation_error",
            started_at=started_at,
            fallback_reason=None,
        )
        _record_audit_event(
            settings=settings,
            request_id=request_id,
            source=source,
            file_type=file_type,
            input_chars=0,
            provider_attempts=[],
            final_provider="none",
            status_label="validation_error",
            started_at=started_at,
            fallback_reason=None,
            redaction_summary={},
        )
        _raise_http_error(
            header_name=settings.audit_request_id_header,
            request_id=request_id,
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail=str(exc),
        )
    except (UnsupportedFileTypeError, FileTypeMismatchError) as exc:
        operational_metrics.record_request_outcome("validation_error")
        _log_request(
            request_id=request_id,
            source=source,
            file_type=file_type,
            input_chars=0,
            provider="none",
            status_label="validation_error",
            started_at=started_at,
            fallback_reason=None,
        )
        _record_audit_event(
            settings=settings,
            request_id=request_id,
            source=source,
            file_type=file_type,
            input_chars=0,
            provider_attempts=[],
            final_provider="none",
            status_label="validation_error",
            started_at=started_at,
            fallback_reason=None,
            redaction_summary={},
        )
        _raise_http_error(
            header_name=settings.audit_request_id_header,
            request_id=request_id,
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=str(exc),
        )
    except FileDecodingError as exc:
        operational_metrics.record_request_outcome("validation_error")
        _log_request(
            request_id=request_id,
            source=source,
            file_type=file_type,
            input_chars=0,
            provider="none",
            status_label="validation_error",
            started_at=started_at,
            fallback_reason=None,
        )
        _record_audit_event(
            settings=settings,
            request_id=request_id,
            source=source,
            file_type=file_type,
            input_chars=0,
            provider_attempts=[],
            final_provider="none",
            status_label="validation_error",
            started_at=started_at,
            fallback_reason=None,
            redaction_summary={},
        )
        _raise_http_error(
            header_name=settings.audit_request_id_header,
            request_id=request_id,
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except IngestionError as exc:  # pragma: no cover - defensive guard
        operational_metrics.record_request_outcome("validation_error")
        _log_request(
            request_id=request_id,
            source=source,
            file_type=file_type,
            input_chars=0,
            provider="none",
            status_label="validation_error",
            started_at=started_at,
            fallback_reason=None,
        )
        _record_audit_event(
            settings=settings,
            request_id=request_id,
            source=source,
            file_type=file_type,
            input_chars=0,
            provider_attempts=[],
            final_provider="none",
            status_label="validation_error",
            started_at=started_at,
            fallback_reason=None,
            redaction_summary={},
        )
        _raise_http_error(
            header_name=settings.audit_request_id_header,
            request_id=request_id,
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    analysis_result, audit_trace = analyze_ingested_content_with_trace(
        ingested_content,
        settings=settings,
        request_id=request_id,
    )
    status_label = (
        "provider_fallback" if analysis_result.provider.startswith("fallback:") else "success"
    )
    operational_metrics.record_request_outcome(status_label)
    _log_request(
        request_id=request_id,
        source=ingested_content.source,
        file_type=ingested_content.file_type or "none",
        input_chars=len(ingested_content.text),
        provider=analysis_result.provider,
        status_label=status_label,
        started_at=started_at,
        fallback_reason=derive_fallback_reason(analysis_result.provider),
    )
    _record_audit_event(
        settings=settings,
        request_id=request_id,
        source=ingested_content.source,
        file_type=ingested_content.file_type or "none",
        input_chars=len(ingested_content.text),
        provider_attempts=list(audit_trace.provider_attempts),
        final_provider=audit_trace.final_provider,
        status_label=status_label,
        started_at=started_at,
        fallback_reason=audit_trace.fallback_reason,
        redaction_summary=audit_trace.redaction_summary,
    )
    return AnalyzeResponse(**analysis_result.as_dict())


def _extract_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    if request.client and request.client.host:
        return request.client.host
    return "unknown"


def _sanitize_file_type(file_name: str | None) -> str:
    if not file_name or "." not in file_name:
        return "unknown"
    return file_name.rsplit(".", maxsplit=1)[-1].lower()


def _raise_http_error(*, header_name: str, request_id: str, status_code: int, detail: str) -> None:
    raise HTTPException(
        status_code=status_code,
        detail=detail,
        headers={header_name: request_id},
    )


def _log_request(
    *,
    request_id: str,
    source: str,
    file_type: str,
    input_chars: int,
    provider: str,
    status_label: str,
    started_at: float,
    fallback_reason: str | None,
) -> None:
    duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
    log_analysis_event(
        request_id=request_id,
        source=source,
        file_type=file_type,
        input_chars=input_chars,
        provider=provider,
        status=status_label,
        fallback_reason=fallback_reason,
        duration_ms=duration_ms,
    )


def _record_audit_event(
    *,
    settings,
    request_id: str,
    source: str,
    file_type: str,
    input_chars: int,
    provider_attempts: list[dict[str, object]],
    final_provider: str,
    status_label: str,
    started_at: float,
    fallback_reason: str | None,
    redaction_summary: dict[str, int],
) -> None:
    if not settings.audit_trace_enabled:
        return

    duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
    audit_trail.record_event(
        {
            "request_id": request_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": status_label,
            "source": source,
            "file_type": file_type,
            "input_chars": input_chars,
            "provider_attempts": provider_attempts,
            "final_provider": final_provider,
            "fallback_reason": fallback_reason,
            "redaction_summary": redaction_summary,
            "duration_ms": duration_ms,
        },
        max_events=settings.audit_recent_events_limit,
        maxlen=settings.audit_event_maxlen,
    )
