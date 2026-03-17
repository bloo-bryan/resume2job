from spacy.language import Language

from resume2job.extraction.skills import classify_jd_skills, extract_skills


class TestExtractSkills:
    def test_finds_known_skills(self, nlp_pipeline: Language) -> None:
        text = "Experience with Python, machine learning, and Docker."
        skills = extract_skills(text, nlp_pipeline)
        assert len(skills) > 0

    def test_deduplication(self, nlp_pipeline: Language) -> None:
        text = "Python is great. I love Python."
        skills = extract_skills(text, nlp_pipeline)
        python_count = sum(1 for s in skills if "python" in s.lower())
        assert python_count <= 1

    def test_case_insensitive(self, nlp_pipeline: Language) -> None:
        text_lower = "experience with python and docker"
        text_upper = "Experience with PYTHON and DOCKER"
        skills_lower = extract_skills(text_lower, nlp_pipeline)
        skills_upper = extract_skills(text_upper, nlp_pipeline)
        assert set(skills_lower) == set(skills_upper)

    def test_empty_text(self, nlp_pipeline: Language) -> None:
        skills = extract_skills("", nlp_pipeline)
        assert skills == []

    def test_returns_sorted_list(self, nlp_pipeline: Language) -> None:
        text = "Python, Docker, machine learning, SQL"
        skills = extract_skills(text, nlp_pipeline)
        assert skills == sorted(skills)


class TestClassifyJdSkills:
    def test_splits_required_preferred(self, nlp_pipeline: Language) -> None:
        text = "Requirements:\n- Python\n- SQL\n\nNice to Have:\n- Kubernetes\n"
        required, preferred = classify_jd_skills(text, nlp_pipeline)
        assert len(required) > 0 or len(preferred) > 0

    def test_no_preferred_section(self, nlp_pipeline: Language) -> None:
        text = "Requirements:\n- Python\n- SQL\n"
        required, preferred = classify_jd_skills(text, nlp_pipeline)
        assert preferred == []

    def test_no_overlap(self, nlp_pipeline: Language) -> None:
        text = "Requirements:\n- Python\n- SQL\n\nNice to Have:\n- Python\n- Kubernetes\n"
        required, preferred = classify_jd_skills(text, nlp_pipeline)
        overlap = set(required) & set(preferred)
        assert len(overlap) == 0

    def test_empty_text(self, nlp_pipeline: Language) -> None:
        required, preferred = classify_jd_skills("", nlp_pipeline)
        assert required == []
        assert preferred == []
