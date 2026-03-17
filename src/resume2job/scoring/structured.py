from resume2job.extraction.education import DEGREE_RANK
from resume2job.models import (
    EducationBreakdown,
    EducationEntry,
    ExperienceBreakdown,
    JobDescriptionEntities,
    ResumeEntities,
    SkillsBreakdown,
)


def _score_skills(resume_skills: list[str], jd_skills: list[str]) -> SkillsBreakdown:
    if not jd_skills:
        return SkillsBreakdown(score=1.0, matched=[], missing=[])

    resume_set = {s.lower() for s in resume_skills}
    matched = [s for s in jd_skills if s.lower() in resume_set]
    missing = [s for s in jd_skills if s.lower() not in resume_set]
    score = len(matched) / len(jd_skills)

    return SkillsBreakdown(score=score, matched=matched, missing=missing)


def _score_experience(total_years: float, required_years: float | None) -> ExperienceBreakdown:
    if required_years is None or required_years <= 0:
        return ExperienceBreakdown(score=1.0, required=required_years, detected=total_years)

    score = min(total_years / required_years, 1.0)
    return ExperienceBreakdown(score=score, required=required_years, detected=total_years)


def _score_education(
    resume_education: list[EducationEntry], required_education: str | None
) -> EducationBreakdown:
    if not required_education:
        return EducationBreakdown(score=1.0, required=None, detected=None)

    required_rank = DEGREE_RANK.get(required_education, 0)

    detected_degree: str | None = None
    detected_rank = 0
    for edu in resume_education:
        rank = DEGREE_RANK.get(edu.degree, 0)
        if rank > detected_rank:
            detected_rank = rank
            detected_degree = edu.degree

    if detected_rank == 0:
        score = 0.0
    elif detected_rank >= required_rank:
        score = 1.0
    else:
        score = detected_rank / required_rank

    return EducationBreakdown(score=score, required=required_education, detected=detected_degree)


def score_structured(
    resume: ResumeEntities,
    jd: JobDescriptionEntities,
) -> dict[str, SkillsBreakdown | ExperienceBreakdown | EducationBreakdown]:
    return {
        "required_skills": _score_skills(resume.skills, jd.required_skills),
        "preferred_skills": _score_skills(resume.skills, jd.preferred_skills),
        "experience": _score_experience(resume.experience.total_years, jd.min_experience_years),
        "education": _score_education(resume.education, jd.required_education),
    }
