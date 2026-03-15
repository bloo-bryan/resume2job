from pathlib import Path

import pytest

from resume2job.parser.pdf import extract_text_from_pdf

FIXTURES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "samples" / "fixtures"
SAMPLE_PDF = FIXTURES_DIR / "sample_resume.pdf"


@pytest.mark.skipif(not SAMPLE_PDF.exists(), reason="sample_resume.pdf fixture not found")
class TestExtractTextFromPdf:
    def test_extracted_text_is_non_empty(self) -> None:
        file_bytes = SAMPLE_PDF.read_bytes()
        text = extract_text_from_pdf(file_bytes)
        assert len(text.strip()) > 0

    def test_contains_expected_content(self) -> None:
        file_bytes = SAMPLE_PDF.read_bytes()
        text = extract_text_from_pdf(file_bytes)
        assert "Sarah Chen" in text
