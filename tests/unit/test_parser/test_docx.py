from pathlib import Path

import pytest

from resume2job.parser.docx_parser import extract_text_from_docx

FIXTURES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "samples" / "fixtures"
SAMPLE_DOCX = FIXTURES_DIR / "sample_resume.docx"


@pytest.mark.skipif(not SAMPLE_DOCX.exists(), reason="sample_resume.docx fixture not found")
class TestExtractTextFromDocx:
    def test_extracted_text_is_non_empty(self) -> None:
        file_bytes = SAMPLE_DOCX.read_bytes()
        text = extract_text_from_docx(file_bytes)
        assert len(text.strip()) > 0

    def test_contains_expected_content(self) -> None:
        file_bytes = SAMPLE_DOCX.read_bytes()
        text = extract_text_from_docx(file_bytes)
        # Basic check that some content was extracted
        assert len(text) > 50
