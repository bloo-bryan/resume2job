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


class SkillsBreakdown(BaseModel):
    score: float
    matched: list[str]
    missing: list[str]


class ExperienceBreakdown(BaseModel):
    score: float
    required: float | None = None
    detected: float


class EducationBreakdown(BaseModel):
    score: float
    required: str | None = None
    detected: str | None = None


class MatchBreakdown(BaseModel):
    required_skills: SkillsBreakdown
    preferred_skills: SkillsBreakdown
    semantic_similarity: float
    experience: ExperienceBreakdown
    education: EducationBreakdown


class MatchResult(BaseModel):
    overall_score: float
    breakdown: MatchBreakdown
    summary: str


class CompareResult(BaseModel):
    tfidf: MatchResult
    embedding: MatchResult
    hybrid: MatchResult
