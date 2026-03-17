from resume2job.models import (
    CompareResult,
    JobDescriptionEntities,
    MatchResult,
    ResumeEntities,
)
from resume2job.scoring.composite import score_embedding_only, score_hybrid, score_tfidf_only
from resume2job.scoring.embedding import score_embedding as score_embedding
from resume2job.scoring.structured import score_structured as score_structured
from resume2job.scoring.tfidf import score_tfidf as score_tfidf


def match(
    resume_text: str,
    jd_text: str,
    resume_entities: ResumeEntities,
    jd_entities: JobDescriptionEntities,
    algorithm: str = "hybrid",
) -> MatchResult:
    if algorithm == "tfidf":
        return score_tfidf_only(resume_text, jd_text, resume_entities, jd_entities)
    elif algorithm == "embedding":
        return score_embedding_only(resume_text, jd_text, resume_entities, jd_entities)
    elif algorithm == "hybrid":
        return score_hybrid(resume_text, jd_text, resume_entities, jd_entities)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}. Use 'tfidf', 'embedding', or 'hybrid'.")


def compare(
    resume_text: str,
    jd_text: str,
    resume_entities: ResumeEntities,
    jd_entities: JobDescriptionEntities,
) -> CompareResult:
    return CompareResult(
        tfidf=score_tfidf_only(resume_text, jd_text, resume_entities, jd_entities),
        embedding=score_embedding_only(resume_text, jd_text, resume_entities, jd_entities),
        hybrid=score_hybrid(resume_text, jd_text, resume_entities, jd_entities),
    )
