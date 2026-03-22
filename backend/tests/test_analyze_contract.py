from __future__ import annotations

import asyncio
import logging
from pathlib import Path

import pytest
from fastapi import HTTPException, Response
from starlette.requests import Request

from app.api.analyze import analyze_email, health_check
from app.api.ops import audit_trail_snapshot
from app.schemas import Category

FIXTURES_DIR = Path(__file__).with_name("fixtures")
SAMPLE_TEXT = FIXTURES_DIR.joinpath("sample_email.txt").read_text(encoding="utf-8")

EXPECTED_KEYS = {
    "category",
    "confidence",
    "rationale",
    "suggested_reply",
    "keywords",
    "provider",
}


class FakeUploadFile:
    def __init__(self, filename: str, content: bytes) -> None:
        self.filename = filename
        self._content = content

    async def read(self) -> bytes:
        return self._content


def _build_request(
    *,
    client_host: str = "127.0.0.1",
    headers: dict[str, str] | None = None,
) -> Request:
    encoded_headers = [
        (key.lower().encode("latin-1"), value.encode("latin-1"))
        for key, value in (headers or {}).items()
    ]
    scope = {
        "type": "http",
        "headers": encoded_headers,
        "client": (client_host, 12345),
        "method": "POST",
        "path": "/analyze",
    }
    return Request(scope)


def _build_response() -> Response:
    return Response()


def _assert_success_payload(payload: dict[str, object]) -> None:
    assert EXPECTED_KEYS.issubset(payload)
    assert isinstance(payload["category"], str)
    assert payload["category"] in {Category.productive.value, Category.unproductive.value}
    assert isinstance(payload["confidence"], (int, float))
    assert 0 <= float(payload["confidence"]) <= 1
    assert isinstance(payload["rationale"], str) and payload["rationale"]
    assert isinstance(payload["suggested_reply"], str) and payload["suggested_reply"]
    assert isinstance(payload["keywords"], list)
    assert isinstance(payload["provider"], str) and payload["provider"]


def _build_minimal_pdf(text: str, *, pages: int = 1) -> bytes:
    header = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
    objects: list[tuple[int, str]] = []

    page_object_numbers: list[int] = []
    catalog_object_number = 1
    pages_object_number = 2
    font_object_number = 3
    next_object_number = 4

    for page_index in range(pages):
        page_object_number = next_object_number
        next_object_number += 1
        content_object_number = next_object_number
        next_object_number += 1
        page_object_numbers.append(page_object_number)

        escaped_text = (
            f"{text} pagina {page_index + 1}".replace("\\", "\\\\")
            .replace("(", "\\(")
            .replace(")", "\\)")
            .replace("\r", " ")
            .replace("\n", " ")
        )
        stream = f"BT /F1 12 Tf 72 720 Td ({escaped_text}) Tj ET\n"

        objects.append(
            (
                page_object_number,
                (
                    f"{page_object_number} 0 obj << /Type /Page "
                    f"/Parent {pages_object_number} 0 R "
                    "/MediaBox [0 0 612 792] /Resources << /Font << "
                    f"/F1 {font_object_number} 0 R >> >> "
                    f"/Contents {content_object_number} 0 R >> endobj\n"
                ),
            )
        )
        objects.append(
            (
                content_object_number,
                (
                    f"{content_object_number} 0 obj << "
                    f"/Length {len(stream.encode('utf-8'))} >> stream\n"
                    f"{stream}endstream endobj\n"
                ),
            )
        )

    kids = " ".join(f"{page_number} 0 R" for page_number in page_object_numbers)
    objects.extend(
        [
            (
                catalog_object_number,
                (
                    f"{catalog_object_number} 0 obj << /Type /Catalog "
                    f"/Pages {pages_object_number} 0 R >> endobj\n"
                ),
            ),
            (
                pages_object_number,
                (
                    f"{pages_object_number} 0 obj << /Type /Pages /Kids [{kids}] "
                    f"/Count {pages} >> endobj\n"
                ),
            ),
            (
                font_object_number,
                (
                    f"{font_object_number} 0 obj << /Type /Font /Subtype /Type1 "
                    "/BaseFont /Helvetica >> endobj\n"
                ),
            ),
        ]
    )
    objects.sort(key=lambda item: item[0])

    chunks = [header]
    offsets = {0: 0}
    current_offset = len(header)

    for object_number, object_text in objects:
        offsets[object_number] = current_offset
        encoded = object_text.encode("ascii")
        chunks.append(encoded)
        current_offset += len(encoded)

    xref_offset = current_offset
    xref_lines = ["xref\n", f"0 {len(objects) + 1}\n", "0000000000 65535 f \n"]
    for object_number in range(1, len(objects) + 1):
        xref_lines.append(f"{offsets[object_number]:010d} 00000 n \n")

    trailer = (
        f"trailer << /Size {len(objects) + 1} /Root {catalog_object_number} 0 R >>\n"
        f"startxref\n{xref_offset}\n"
        "%%EOF\n"
    )

    chunks.append("".join(xref_lines).encode("ascii"))
    chunks.append(trailer.encode("ascii"))
    return b"".join(chunks)


def test_health() -> None:
    assert asyncio.run(health_check()) == {
        "status": "ok",
        "service": "inbox-pilot-backend",
    }


def test_analyze_accepts_text_only() -> None:
    response = _build_response()
    result = asyncio.run(
        analyze_email(
            request=_build_request(),
            response=response,
            email_text=SAMPLE_TEXT,
            email_file=None,
        )
    )

    _assert_success_payload(result.model_dump())
    assert "X-Request-ID" in response.headers


def test_analyze_reuses_request_id_header_when_provided() -> None:
    response = _build_response()
    result = asyncio.run(
        analyze_email(
            request=_build_request(headers={"X-Request-ID": "trace-123"}),
            response=response,
            email_text=SAMPLE_TEXT,
            email_file=None,
        )
    )

    _assert_success_payload(result.model_dump())
    assert response.headers["X-Request-ID"] == "trace-123"


def test_analyze_accepts_txt_upload() -> None:
    response = asyncio.run(
        analyze_email(
            request=_build_request(),
            response=_build_response(),
            email_text=None,
            email_file=FakeUploadFile("sample_email.txt", SAMPLE_TEXT.encode("utf-8")),
        )
    )

    _assert_success_payload(response.model_dump())


def test_analyze_accepts_pdf_upload() -> None:
    response = asyncio.run(
        analyze_email(
            request=_build_request(),
            response=_build_response(),
            email_text=None,
            email_file=FakeUploadFile("sample_email.pdf", _build_minimal_pdf(SAMPLE_TEXT)),
        )
    )

    _assert_success_payload(response.model_dump())


def test_analyze_prefers_file_when_both_inputs_are_present() -> None:
    response = asyncio.run(
        analyze_email(
            request=_build_request(),
            response=_build_response(),
            email_text="This text is present only as a fallback.",
            email_file=FakeUploadFile("sample_email.txt", SAMPLE_TEXT.encode("utf-8")),
        )
    )

    _assert_success_payload(response.model_dump())


def test_analyze_rejects_empty_input() -> None:
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            analyze_email(
                request=_build_request(),
                response=_build_response(),
                email_text=None,
                email_file=None,
            )
        )

    assert exc_info.value.status_code == 400


def test_analyze_rejects_unsupported_file_type() -> None:
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            analyze_email(
                request=_build_request(),
                response=_build_response(),
                email_text=None,
                email_file=FakeUploadFile("sample_email.md", b"# Not supported"),
            )
        )

    assert exc_info.value.status_code == 415


def test_analyze_reports_parse_failure_for_broken_pdf() -> None:
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            analyze_email(
                request=_build_request(),
                response=_build_response(),
                email_text=None,
                email_file=FakeUploadFile("broken.pdf", b"%PDF-bad"),
            )
        )

    assert exc_info.value.status_code == 400


def test_analyze_rejects_oversized_text() -> None:
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            analyze_email(
                request=_build_request(),
                response=_build_response(),
                email_text="a" * 12_001,
                email_file=None,
            )
        )

    assert exc_info.value.status_code == 413


def test_analyze_rejects_oversized_upload() -> None:
    oversized_payload = b"a" * (1_048_576 + 1)
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            analyze_email(
                request=_build_request(),
                response=_build_response(),
                email_text=None,
                email_file=FakeUploadFile("big.txt", oversized_payload),
            )
        )

    assert exc_info.value.status_code == 413


def test_analyze_rejects_pdf_content_with_txt_extension() -> None:
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            analyze_email(
                request=_build_request(),
                response=_build_response(),
                email_text=None,
                email_file=FakeUploadFile("mismatch.txt", _build_minimal_pdf(SAMPLE_TEXT)),
            )
        )

    assert exc_info.value.status_code == 415


def test_analyze_rejects_pdf_above_page_limit() -> None:
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            analyze_email(
                request=_build_request(),
                response=_build_response(),
                email_text=None,
                email_file=FakeUploadFile(
                    "too-many-pages.pdf",
                    _build_minimal_pdf(SAMPLE_TEXT, pages=11),
                ),
            )
        )

    assert exc_info.value.status_code == 413


def test_analyze_rate_limit_returns_429() -> None:
    for _ in range(20):
        response = asyncio.run(
            analyze_email(
                request=_build_request(client_host="192.168.0.8"),
                response=_build_response(),
                email_text=SAMPLE_TEXT,
                email_file=None,
            )
        )
        _assert_success_payload(response.model_dump())

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            analyze_email(
                request=_build_request(client_host="192.168.0.8"),
                response=_build_response(),
                email_text=SAMPLE_TEXT,
                email_file=None,
            )
        )

    assert exc_info.value.status_code == 429
    assert 1 <= int(exc_info.value.headers["Retry-After"]) <= 60


def test_analysis_logs_do_not_include_raw_email(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO, logger="app.security")

    response = asyncio.run(
        analyze_email(
            request=_build_request(headers={"x-request-id": "test-request-id"}),
            response=_build_response(),
            email_text=SAMPLE_TEXT,
            email_file=None,
        )
    )

    _assert_success_payload(response.model_dump())
    assert "test-request-id" in caplog.text
    assert SAMPLE_TEXT not in caplog.text
    assert '"status": "provider_fallback"' in caplog.text


def test_audit_trail_does_not_expose_filename_or_suggested_reply() -> None:
    response = _build_response()
    result = asyncio.run(
        analyze_email(
            request=_build_request(headers={"X-Request-ID": "audit-file-test"}),
            response=response,
            email_text=None,
            email_file=FakeUploadFile(
                "customer_invoice_9981_sensitive.txt",
                SAMPLE_TEXT.encode("utf-8"),
            ),
        )
    )

    _assert_success_payload(result.model_dump())
    payload = asyncio.run(audit_trail_snapshot())
    event = payload["events"][0]

    assert payload["count"] == 1
    assert event["request_id"] == "audit-file-test"
    assert "customer_invoice_9981_sensitive.txt" not in str(event)
    assert result.suggested_reply not in str(event)
