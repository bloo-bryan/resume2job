from spacy.language import Language

from resume2job.extraction.education import (
    DEGREE_RANK,
    extract_education,
    extract_required_education,
)


class TestExtractEducation:
    def test_detects_ms_degree(self, nlp_pipeline: Language) -> None:
        text = "M.S. in Computer Science from Stanford University"
        entries = extract_education(text, nlp_pipeline)
        degrees = [e.degree for e in entries]
        assert "M.S." in degrees

    def test_detects_bs_degree(self, nlp_pipeline: Language) -> None:
        text = "B.S. in Mathematics from UC Berkeley"
        entries = extract_education(text, nlp_pipeline)
        degrees = [e.degree for e in entries]
        assert "B.S." in degrees

    def test_detects_phd(self, nlp_pipeline: Language) -> None:
        text = "Ph.D. in Machine Learning from MIT"
        entries = extract_education(text, nlp_pipeline)
        degrees = [e.degree for e in entries]
        assert "Ph.D." in degrees

    def test_detects_mba(self, nlp_pipeline: Language) -> None:
        text = "MBA from Harvard Business School"
        entries = extract_education(text, nlp_pipeline)
        degrees = [e.degree for e in entries]
        assert "MBA" in degrees

    def test_detects_associate(self, nlp_pipeline: Language) -> None:
        text = "Associate's degree in Applied Science"
        entries = extract_education(text, nlp_pipeline)
        degrees = [e.degree for e in entries]
        assert "Associate" in degrees

    def test_field_extraction(self, nlp_pipeline: Language) -> None:
        text = "M.S. in Computer Science from Stanford University"
        entries = extract_education(text, nlp_pipeline)
        ms_entries = [e for e in entries if e.degree == "M.S."]
        assert len(ms_entries) == 1
        assert ms_entries[0].field is not None
        assert "Computer Science" in ms_entries[0].field

    def test_deduplication(self, nlp_pipeline: Language) -> None:
        text = "M.S. in Computer Science from Stanford University\nM.S. in Data Science from MIT\n"
        entries = extract_education(text, nlp_pipeline)
        ms_count = sum(1 for e in entries if e.degree == "M.S.")
        assert ms_count == 1

    def test_sorted_by_rank_descending(self, nlp_pipeline: Language) -> None:
        text = (
            "B.S. in Mathematics from UC Berkeley\n"
            "Ph.D. in Computer Science from Stanford\n"
            "M.S. in Statistics from MIT\n"
        )
        entries = extract_education(text, nlp_pipeline)
        ranks = [DEGREE_RANK.get(e.degree, 0) for e in entries]
        assert ranks == sorted(ranks, reverse=True)

    def test_empty_text(self, nlp_pipeline: Language) -> None:
        entries = extract_education("", nlp_pipeline)
        assert entries == []


class TestExtractRequiredEducation:
    def test_finds_highest_degree(self) -> None:
        text = "M.S. in Computer Science required. Ph.D. preferred."
        result = extract_required_education(text)
        assert result == "Ph.D."

    def test_single_degree(self) -> None:
        text = "Bachelor's degree in Computer Science or related field"
        result = extract_required_education(text)
        assert result in ("B.S.", "B.A.")

    def test_no_degree_returns_none(self) -> None:
        text = "We are looking for a talented engineer."
        result = extract_required_education(text)
        assert result is None
