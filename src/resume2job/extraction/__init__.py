from spacy.language import Language

from resume2job.extraction.education import extract_education, extract_required_education
from resume2job.extraction.experience import extract_experience, extract_min_experience_years
from resume2job.extraction.ner import build_nlp_pipeline
from resume2job.extraction.skills import classify_jd_skills, extract_skills
from resume2job.models import (
    JobDescriptionEntities,
    ParseResult,
    ResumeEntities,
)


def extract_resume_entities(cleaned_text: str, nlp: Language | None = None) -> ResumeEntities:
    if nlp is None:
        nlp = build_nlp_pipeline()

    skills = extract_skills(cleaned_text, nlp)
    experience = extract_experience(cleaned_text)
    education = extract_education(cleaned_text, nlp)

    return ResumeEntities(
        skills=skills,
        experience=experience,
        education=education,
    )


def extract_jd_entities(cleaned_text: str, nlp: Language | None = None) -> JobDescriptionEntities:
    if nlp is None:
        nlp = build_nlp_pipeline()

    required_skills, preferred_skills = classify_jd_skills(cleaned_text, nlp)
    min_experience_years = extract_min_experience_years(cleaned_text)
    required_education = extract_required_education(cleaned_text)

    return JobDescriptionEntities(
        required_skills=required_skills,
        preferred_skills=preferred_skills,
        min_experience_years=min_experience_years,
        required_education=required_education,
    )


def parse_and_extract(
    raw_text: str,
    cleaned_text: str,
    doc_type: str,
    nlp: Language | None = None,
) -> ParseResult:
    if doc_type == "resume":
        entities = extract_resume_entities(cleaned_text, nlp)
    elif doc_type == "job_description":
        entities = extract_jd_entities(cleaned_text, nlp)
    else:
        raise ValueError(f"Unknown doc_type: {doc_type}. Use 'resume' or 'job_description'.")

    return ParseResult(
        raw_text=raw_text,
        cleaned_text=cleaned_text,
        doc_type=doc_type,
        entities=entities,
    )
