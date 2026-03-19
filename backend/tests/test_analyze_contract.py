from __future__ import annotations

import asyncio
from pathlib import Path

from app.api.analyze import analyze_email, health_check
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


def _build_minimal_pdf(text: str) -> bytes:
    escaped_text = (
        text.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .replace("\r", " ")
        .replace("\n", " ")
    )
    stream = f"BT /F1 12 Tf 72 720 Td ({escaped_text}) Tj ET\n"
    header = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"

    objects = [
        "1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n",
        "2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n",
        (
            "3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            "/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n"
        ),
        "4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n",
        (
            f"5 0 obj << /Length {len(stream.encode('utf-8'))} >> stream\n"
            f"{stream}endstream endobj\n"
        ),
    ]

    chunks = [header]
    offsets = {0: 0}
    current_offset = len(header)

    for object_number, object_text in enumerate(objects, start=1):
        offsets[object_number] = current_offset
        encoded = object_text.encode("ascii")
        chunks.append(encoded)
        current_offset += len(encoded)

    xref_offset = current_offset
    xref_lines = ["xref\n", "0 6\n", "0000000000 65535 f \n"]
    for object_number in range(1, 6):
        xref_lines.append(f"{offsets[object_number]:010d} 00000 n \n")

    trailer = (
        "trailer << /Size 6 /Root 1 0 R >>\n"
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
    response = asyncio.run(analyze_email(email_text=SAMPLE_TEXT, email_file=None))

    _assert_success_payload(response.model_dump())


def test_analyze_accepts_txt_upload() -> None:
    response = asyncio.run(
        analyze_email(
            email_text=None,
            email_file=FakeUploadFile(
                "sample_email.txt",
                SAMPLE_TEXT.encode("utf-8"),
            ),
        )
    )

    _assert_success_payload(response.model_dump())


def test_analyze_accepts_pdf_upload() -> None:
    response = asyncio.run(
        analyze_email(
            email_text=None,
            email_file=FakeUploadFile(
                "sample_email.pdf",
                _build_minimal_pdf(SAMPLE_TEXT),
            ),
        )
    )

    _assert_success_payload(response.model_dump())


def test_analyze_prefers_file_when_both_inputs_are_present() -> None:
    response = asyncio.run(
        analyze_email(
            email_text="This text is present only as a fallback.",
            email_file=FakeUploadFile(
                "sample_email.txt",
                SAMPLE_TEXT.encode("utf-8"),
            ),
        )
    )

    _assert_success_payload(response.model_dump())


def test_analyze_rejects_empty_input() -> None:
    try:
        asyncio.run(analyze_email(email_text=None, email_file=None))
    except Exception as exc:  # noqa: BLE001
        assert type(exc).__name__ in {"HTTPException", "EmptyInputError"}
    else:  # pragma: no cover - defensive guard
        raise AssertionError("empty input should fail")


def test_analyze_rejects_unsupported_file_type() -> None:
    try:
        asyncio.run(
            analyze_email(
                email_text=None,
                email_file=FakeUploadFile("sample_email.md", b"# Not supported"),
            )
        )
    except Exception as exc:  # noqa: BLE001
        assert type(exc).__name__ in {"HTTPException", "UnsupportedFileTypeError"}
    else:  # pragma: no cover - defensive guard
        raise AssertionError("unsupported file should fail")


def test_analyze_reports_parse_failure_for_broken_pdf() -> None:
    try:
        asyncio.run(
            analyze_email(
                email_text=None,
                email_file=FakeUploadFile("broken.pdf", b"not-a-real-pdf"),
            )
        )
    except Exception as exc:  # noqa: BLE001
        assert type(exc).__name__ in {"HTTPException", "FileDecodingError"}
    else:  # pragma: no cover - defensive guard
        raise AssertionError("broken PDF should fail")
