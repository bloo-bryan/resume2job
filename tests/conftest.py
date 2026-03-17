from pathlib import Path

import pytest

SAMPLES_DIR = Path(__file__).resolve().parent.parent / "data" / "samples"


@pytest.fixture
def sample_resume_text() -> str:
    return (SAMPLES_DIR / "resumes" / "resume_01_ml_engineer_senior.txt").read_text()


@pytest.fixture
def sample_jd_text() -> str:
    return (SAMPLES_DIR / "job_descriptions" / "jd_01_senior_ml_engineer.txt").read_text()


@pytest.fixture(scope="session")
def nlp_pipeline():
    from resume2job.extraction.ner import build_nlp_pipeline

    return build_nlp_pipeline()
