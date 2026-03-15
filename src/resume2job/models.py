from pydantic import BaseModel


class Position(BaseModel):
    title: str
    company: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    years: float | None = None


class ExperienceInfo(BaseModel):
    total_years: float
    positions: list[Position]


class EducationEntry(BaseModel):
    degree: str
    field: str | None = None
    institution: str | None = None


class ResumeEntities(BaseModel):
    skills: list[str]
    experience: ExperienceInfo
    education: list[EducationEntry]


class JobDescriptionEntities(BaseModel):
    required_skills: list[str]
    preferred_skills: list[str]
    min_experience_years: float | None = None
    required_education: str | None = None


class ParseResult(BaseModel):
    raw_text: str
    cleaned_text: str
    entities: ResumeEntities | JobDescriptionEntities
