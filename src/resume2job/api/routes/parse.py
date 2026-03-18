from fastapi import APIRouter, Form, HTTPException, UploadFile

from resume2job.config import get_settings
from resume2job.extraction import parse_and_extract
from resume2job.models import ParseResult
from resume2job.parser import parse_document

router = APIRouter()


@router.post("/api/parse", response_model=ParseResult)
async def parse(
    doc_type: str = Form(...),
    text: str | None = Form(None),
    file: UploadFile | None = None,
) -> ParseResult:
    if text and file:
        raise HTTPException(status_code=400, detail="Provide either text or file, not both.")
    if not text and not file:
        raise HTTPException(status_code=400, detail="Provide either text or file.")
    if doc_type not in ("resume", "job_description"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid doc_type: {doc_type}. Use 'resume' or 'job_description'.",
        )

    if file:
        settings = get_settings()
        file_bytes = await file.read()
        max_bytes = settings.max_upload_size_mb * 1024 * 1024
        if len(file_bytes) > max_bytes:
            raise HTTPException(
                status_code=400,
                detail=f"File exceeds {settings.max_upload_size_mb}MB limit.",
            )
        raw_text, cleaned_text = parse_document(file_bytes, file.filename or "")
    else:
        raw_text, cleaned_text = parse_document(None, "", raw_text=text)

    return parse_and_extract(raw_text, cleaned_text, doc_type)
