from spacy.language import Language

from resume2job.extraction import extract_jd_entities, extract_resume_entities


class TestResumeExtraction:
    def test_full_resume_extraction(self, sample_resume_text: str, nlp_pipeline: Language) -> None:
        result = extract_resume_entities(sample_resume_text, nlp_pipeline)

        assert len(result.skills) > 0, "Should extract at least one skill"
        assert result.experience.total_years > 0, "Should compute positive total years"
        assert len(result.experience.positions) > 0, "Should find at least one position"
        assert len(result.education) > 0, "Should find at least one education entry"

    def test_resume_skills_are_strings(
        self, sample_resume_text: str, nlp_pipeline: Language
    ) -> None:
        result = extract_resume_entities(sample_resume_text, nlp_pipeline)
        for skill in result.skills:
            assert isinstance(skill, str)
            assert len(skill) > 0

    def test_resume_education_sorted(self, sample_resume_text: str, nlp_pipeline: Language) -> None:
        from resume2job.extraction.education import DEGREE_RANK

        result = extract_resume_entities(sample_resume_text, nlp_pipeline)
        if len(result.education) > 1:
            ranks = [DEGREE_RANK.get(e.degree, 0) for e in result.education]
            assert ranks == sorted(ranks, reverse=True)


class TestJdExtraction:
    def test_full_jd_extraction(self, sample_jd_text: str, nlp_pipeline: Language) -> None:
        result = extract_jd_entities(sample_jd_text, nlp_pipeline)

        assert len(result.required_skills) > 0, "Should extract required skills"

    def test_no_overlap_required_preferred(
        self, sample_jd_text: str, nlp_pipeline: Language
    ) -> None:
        result = extract_jd_entities(sample_jd_text, nlp_pipeline)
        overlap = set(result.required_skills) & set(result.preferred_skills)
        assert len(overlap) == 0, f"Skills should not appear in both lists: {overlap}"

    def test_min_experience_extracted(self, sample_jd_text: str, nlp_pipeline: Language) -> None:
        result = extract_jd_entities(sample_jd_text, nlp_pipeline)
        assert result.min_experience_years is not None
        assert result.min_experience_years > 0

    def test_required_education_extracted(
        self, sample_jd_text: str, nlp_pipeline: Language
    ) -> None:
        result = extract_jd_entities(sample_jd_text, nlp_pipeline)
        assert result.required_education is not None
