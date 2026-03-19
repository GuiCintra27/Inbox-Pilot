from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.schemas import AnalyzeResponse
from app.services import (
    EmptyInputError,
    FileDecodingError,
    IngestionError,
    UnsupportedFileTypeError,
    analyze_ingested_content,
    ingest_email_content,
)

router = APIRouter(prefix="")


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "inbox-pilot-backend"}


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_email(
    email_text: Annotated[str | None, Form()] = None,
    email_file: Annotated[UploadFile | None, File()] = None,
) -> AnalyzeResponse:
    try:
        file_content = None
        file_name = None
        if email_file is not None:
            file_name = email_file.filename
            file_content = await email_file.read()
            if not file_content:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="O arquivo enviado está vazio.",
                )

        ingested_content = ingest_email_content(
            email_text=email_text,
            email_file_name=file_name,
            email_file_content=file_content,
        )
    except HTTPException:
        raise
    except (EmptyInputError, UnsupportedFileTypeError, FileDecodingError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except IngestionError as exc:  # pragma: no cover - defensive guard
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    analysis_result = analyze_ingested_content(ingested_content)
    return AnalyzeResponse(**analysis_result.as_dict())
