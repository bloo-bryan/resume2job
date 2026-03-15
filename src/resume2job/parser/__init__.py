from resume2job.parser.docx_parser import extract_text_from_docx
from resume2job.parser.pdf import extract_text_from_pdf
from resume2job.parser.text_cleaner import clean_text


def parse_document(
    file_bytes: bytes | None,
    filename: str,
    raw_text: str | None = None,
) -> tuple[str, str]:
    if file_bytes is None and raw_text is not None:
        return raw_text, clean_text(raw_text)

    if file_bytes is None:
        raise ValueError("Either file_bytes or raw_text must be provided")

    ext = filename.rsplit(".", maxsplit=1)[-1].lower() if "." in filename else ""

    if ext == "pdf":
        raw = extract_text_from_pdf(file_bytes)
    elif ext in ("docx", "doc"):
        raw = extract_text_from_docx(file_bytes)
    else:
        raise ValueError(f"Unsupported file type: .{ext}")

    return raw, clean_text(raw)
