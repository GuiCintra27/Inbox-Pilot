from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

IngestionSource = Literal["text", "txt_file", "pdf_file"]
IngestionFileType = Literal["txt", "pdf"]


@dataclass(frozen=True, slots=True)
class IngestedContent:
    text: str
    source: IngestionSource
    language: str
    language_confidence: float
    file_name: str | None = None
    file_type: IngestionFileType | None = None


class IngestionError(ValueError):
    """Base error for ingestion failures."""


class EmptyInputError(IngestionError):
    """Raised when no usable email content is provided."""


class UnsupportedFileTypeError(IngestionError):
    """Raised when the uploaded file type is not supported."""


class FileDecodingError(IngestionError):
    """Raised when a file cannot be decoded into usable text."""


class InputTooLargeError(IngestionError):
    """Raised when the submitted text or extracted content exceeds limits."""


class FileTypeMismatchError(UnsupportedFileTypeError):
    """Raised when the file extension and the detected payload type do not match."""


class PdfPageLimitError(InputTooLargeError):
    """Raised when a PDF exceeds the configured page limit."""
