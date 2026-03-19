from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Final

from pypdf import PdfReader

from app.core.language import detect_language
from app.core.text import normalize_text
from app.domain.ingestion import (
    EmptyInputError,
    FileDecodingError,
    IngestedContent,
    IngestionError,
    IngestionFileType,
    UnsupportedFileTypeError,
)

_TXT_ENCODINGS: Final[tuple[str, ...]] = ("utf-8-sig", "utf-8", "latin-1", "cp1252")


def ingest_email_content(
    *,
    email_text: str | None = None,
    email_file_name: str | None = None,
    email_file_content: bytes | None = None,
) -> IngestedContent:
    """
    Resolve and normalize the user input for the email analysis flow.

    Rule of precedence:
    - when a file is provided, it takes precedence over free text
    - file extraction errors are surfaced instead of silently falling back
    - free text is only used when no file is provided
    """

    file_provided = email_file_name is not None or email_file_content is not None
    if file_provided:
        if email_file_name is None:
            raise UnsupportedFileTypeError("O nome do arquivo é obrigatório para inferir o tipo.")
        if not _has_file_content(email_file_content):
            raise FileDecodingError("O arquivo enviado está vazio.")

        return ingest_file_content(
            file_name=email_file_name,
            file_content=email_file_content or b"",
        )

    if email_text is not None:
        return ingest_free_text(email_text)

    raise EmptyInputError("Forneça `email_text` ou `email_file` para iniciar a análise.")


def ingest_free_text(email_text: str) -> IngestedContent:
    normalized_text = normalize_text(email_text)
    if not normalized_text:
        raise EmptyInputError("O texto informado está vazio após a normalização.")

    language = detect_language(normalized_text)
    return IngestedContent(
        text=normalized_text,
        source="text",
        language=language.language,
        language_confidence=language.confidence,
    )


def ingest_file_content(*, file_name: str, file_content: bytes) -> IngestedContent:
    file_type = infer_file_type(file_name=file_name, file_content=file_content)

    if file_type == "txt":
        text = extract_text_from_txt(file_content=file_content)
    elif file_type == "pdf":
        text = extract_text_from_pdf(file_content=file_content)
    else:  # pragma: no cover - defensive branch for future extensions
        raise UnsupportedFileTypeError(f"Tipo de arquivo não suportado: {file_name}")

    normalized_text = normalize_text(text)
    if not normalized_text:
        raise FileDecodingError("Não foi possível extrair texto legível do arquivo enviado.")

    language = detect_language(normalized_text)
    return IngestedContent(
        text=normalized_text,
        source="txt_file" if file_type == "txt" else "pdf_file",
        language=language.language,
        language_confidence=language.confidence,
        file_name=file_name,
        file_type=file_type,
    )


def extract_text_from_txt(*, file_content: bytes) -> str:
    last_error: UnicodeDecodeError | None = None

    for encoding in _TXT_ENCODINGS:
        try:
            return file_content.decode(encoding)
        except UnicodeDecodeError as error:
            last_error = error

    if last_error is not None:
        return file_content.decode("utf-8", errors="replace")

    raise FileDecodingError("Não foi possível decodificar o arquivo .txt enviado.")


def extract_text_from_pdf(*, file_content: bytes) -> str:
    try:
        reader = PdfReader(BytesIO(file_content))
    except Exception as error:  # pragma: no cover - pypdf raises several exception types
        raise FileDecodingError("Não foi possível abrir o PDF enviado.") from error

    pages_text: list[str] = []
    for page in reader.pages:
        try:
            page_text = page.extract_text() or ""
        except Exception as error:  # pragma: no cover - defensive against malformed pages
            raise FileDecodingError("Falha ao extrair texto de uma página do PDF.") from error
        if page_text.strip():
            pages_text.append(page_text)

    return "\n\n".join(pages_text)


def infer_file_type(*, file_name: str, file_content: bytes | None = None) -> IngestionFileType:
    suffix = Path(file_name).suffix.lower()
    if suffix == ".txt":
        return "txt"
    if suffix == ".pdf":
        return "pdf"

    if file_content is not None and file_content[:5] == b"%PDF-":
        return "pdf"

    raise UnsupportedFileTypeError(
        "Formato de arquivo não suportado. Use somente arquivos .txt ou .pdf."
    )


def _has_file_content(file_content: bytes | None) -> bool:
    return bool(file_content and file_content.strip())


__all__ = [
    "EmptyInputError",
    "FileDecodingError",
    "IngestedContent",
    "IngestionError",
    "UnsupportedFileTypeError",
    "extract_text_from_pdf",
    "extract_text_from_txt",
    "infer_file_type",
    "ingest_email_content",
    "ingest_file_content",
    "ingest_free_text",
]
