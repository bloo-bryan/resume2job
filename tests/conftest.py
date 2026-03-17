from pathlib import Path

import pytest

from resume2job.models import (
    EducationEntry,
    ExperienceInfo,
    JobDescriptionEntities,
    ResumeEntities,
)

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


@pytest.fixture
def sample_resume_entities() -> ResumeEntities:
    return ResumeEntities(
        skills=["python", "pytorch", "docker", "machine learning", "sql"],
        experience=ExperienceInfo(total_years=5.0, positions=[]),
        education=[EducationEntry(degree="M.S.", field="Computer Science")],
    )


@pytest.fixture
def sample_jd_entities() -> JobDescriptionEntities:
    return JobDescriptionEntities(
        required_skills=["python", "pytorch", "sql", "kubernetes"],
        preferred_skills=["docker", "spark"],
        min_experience_years=3.0,
        required_education="B.S.",
    )
