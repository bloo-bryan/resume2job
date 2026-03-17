from resume2job.models import (
    EducationEntry,
    ExperienceInfo,
    JobDescriptionEntities,
    ResumeEntities,
)
from resume2job.scoring.structured import score_structured


def _make_resume(
    skills: list[str] | None = None,
    years: float = 5.0,
    degree: str = "B.S.",
) -> ResumeEntities:
    return ResumeEntities(
        skills=skills or ["python", "docker"],
        experience=ExperienceInfo(total_years=years, positions=[]),
        education=[EducationEntry(degree=degree)] if degree else [],
    )


def _make_jd(
    required: list[str] | None = None,
    preferred: list[str] | None = None,
    min_years: float | None = 3.0,
    education: str | None = "B.S.",
) -> JobDescriptionEntities:
    return JobDescriptionEntities(
        required_skills=["python", "kubernetes"] if required is None else required,
        preferred_skills=["docker"] if preferred is None else preferred,
        min_experience_years=min_years,
        required_education=education,
    )


class TestScoreSkills:
    def test_full_match(self) -> None:
        result = score_structured(
            _make_resume(skills=["python", "kubernetes"]),
            _make_jd(required=["python", "kubernetes"]),
        )
        assert result["required_skills"].score == 1.0
        assert result["required_skills"].missing == []

    def test_partial_match(self) -> None:
        result = score_structured(_make_resume(skills=["python"]), _make_jd())
        assert result["required_skills"].score == 0.5
        assert result["required_skills"].matched == ["python"]
        assert result["required_skills"].missing == ["kubernetes"]

    def test_no_match(self) -> None:
        result = score_structured(_make_resume(skills=["go", "rust"]), _make_jd())
        assert result["required_skills"].score == 0.0

    def test_no_required_skills(self) -> None:
        result = score_structured(_make_resume(), _make_jd(required=[]))
        assert result["required_skills"].score == 1.0


class TestScoreExperience:
    def test_exceeds_requirement(self) -> None:
        result = score_structured(_make_resume(years=10), _make_jd(min_years=5))
        assert result["experience"].score == 1.0

    def test_meets_requirement(self) -> None:
        result = score_structured(_make_resume(years=3), _make_jd(min_years=3))
        assert result["experience"].score == 1.0

    def test_below_requirement(self) -> None:
        result = score_structured(_make_resume(years=2), _make_jd(min_years=4))
        assert result["experience"].score == 0.5

    def test_no_requirement(self) -> None:
        result = score_structured(_make_resume(years=1), _make_jd(min_years=None))
        assert result["experience"].score == 1.0


class TestScoreEducation:
    def test_meets_requirement(self) -> None:
        result = score_structured(_make_resume(degree="M.S."), _make_jd(education="B.S."))
        assert result["education"].score == 1.0

    def test_exceeds_requirement(self) -> None:
        result = score_structured(_make_resume(degree="Ph.D."), _make_jd(education="M.S."))
        assert result["education"].score == 1.0

    def test_below_requirement(self) -> None:
        result = score_structured(_make_resume(degree="B.S."), _make_jd(education="M.S."))
        assert result["education"].score < 1.0
        assert result["education"].score > 0.0

    def test_no_requirement(self) -> None:
        result = score_structured(_make_resume(degree="B.S."), _make_jd(education=None))
        assert result["education"].score == 1.0
