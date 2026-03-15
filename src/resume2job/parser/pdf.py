import io

import pdfplumber


def extract_text_from_pdf(file_bytes: bytes) -> str:
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        pages: list[str] = []
        for page in pdf.pages:
            text = page.extract_text()
            if text is not None:
                pages.append(text)
        return "\n\n".join(pages)
