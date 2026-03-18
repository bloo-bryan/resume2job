from fastapi import APIRouter, HTTPException

from resume2job.api.schemas import CompareRequest, MatchRequest
from resume2job.extraction import extract_jd_entities, extract_resume_entities
from resume2job.models import CompareResult, MatchResult
from resume2job.parser.text_cleaner import clean_text
from resume2job.scoring import compare, match

router = APIRouter()


@router.post("/api/match", response_model=MatchResult)
def match_endpoint(request: MatchRequest) -> MatchResult:
    cleaned_resume = clean_text(request.resume_text)
    cleaned_jd = clean_text(request.jd_text)
    resume_entities = extract_resume_entities(cleaned_resume)
    jd_entities = extract_jd_entities(cleaned_jd)
    try:
        return match(cleaned_resume, cleaned_jd, resume_entities, jd_entities, request.algorithm)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/api/match/compare", response_model=CompareResult)
def compare_endpoint(request: CompareRequest) -> CompareResult:
    cleaned_resume = clean_text(request.resume_text)
    cleaned_jd = clean_text(request.jd_text)
    resume_entities = extract_resume_entities(cleaned_resume)
    jd_entities = extract_jd_entities(cleaned_jd)
    return compare(cleaned_resume, cleaned_jd, resume_entities, jd_entities)
