from resume2job.config import get_settings
from resume2job.models import (
    JobDescriptionEntities,
    MatchBreakdown,
    MatchResult,
    ResumeEntities,
)
from resume2job.scoring.embedding import score_embedding
from resume2job.scoring.structured import score_structured
from resume2job.scoring.tfidf import score_tfidf


def _generate_summary(score: float, breakdown: MatchBreakdown) -> str:
    pct = round(score * 100)

    if pct >= 80:
        strength = "Strong"
    elif pct >= 60:
        strength = "Good"
    elif pct >= 40:
        strength = "Moderate"
    else:
        strength = "Weak"

    parts = [f"{strength} match ({pct}%)."]

    # Education status
    edu = breakdown.education
    if edu.required is None:
        pass
    elif edu.score >= 1.0:
        parts.append(f"Meets education requirement ({edu.detected}).")
    else:
        parts.append(f"Education gap: {edu.required} required, {edu.detected or 'none'} detected.")

    # Experience status
    exp = breakdown.experience
    if exp.required is None:
        pass
    elif exp.score >= 1.0:
        parts.append(f"Meets experience requirement ({exp.detected:.0f}yr).")
    else:
        parts.append(
            f"Experience gap: {exp.required:.0f}yr required, {exp.detected:.0f}yr detected."
        )

    # Skills status
    req = breakdown.required_skills
    if req.missing:
        parts.append(
            f"Missing {len(req.missing)} of {len(req.matched) + len(req.missing)} "
            f"required skills: {', '.join(req.missing[:5])}."
        )
    elif req.matched:
        parts.append(f"All {len(req.matched)} required skills matched.")

    return " ".join(parts)


def score_hybrid(
    resume_text: str,
    jd_text: str,
    resume_entities: ResumeEntities,
    jd_entities: JobDescriptionEntities,
) -> MatchResult:
    settings = get_settings()

    tfidf_sim = score_tfidf(resume_text, jd_text)
    emb_sim = score_embedding(resume_text, jd_text)
    semantic_score = (
        settings.hybrid_tfidf_weight * tfidf_sim + settings.hybrid_embedding_weight * emb_sim
    )

    structured = score_structured(resume_entities, jd_entities)

    overall = (
        settings.weight_required_skills * structured["required_skills"].score
        + settings.weight_semantic * semantic_score
        + settings.weight_experience * structured["experience"].score
        + settings.weight_education * structured["education"].score
        + settings.weight_preferred_skills * structured["preferred_skills"].score
    )

    breakdown = MatchBreakdown(
        required_skills=structured["required_skills"],
        preferred_skills=structured["preferred_skills"],
        semantic_similarity=semantic_score,
        experience=structured["experience"],
        education=structured["education"],
    )

    summary = _generate_summary(overall, breakdown)

    return MatchResult(overall_score=round(overall, 4), breakdown=breakdown, summary=summary)


def score_tfidf_only(
    resume_text: str,
    jd_text: str,
    resume_entities: ResumeEntities,
    jd_entities: JobDescriptionEntities,
) -> MatchResult:
    settings = get_settings()

    tfidf_score = score_tfidf(resume_text, jd_text)
    structured = score_structured(resume_entities, jd_entities)

    overall = (
        settings.weight_required_skills * structured["required_skills"].score
        + settings.weight_semantic * tfidf_score
        + settings.weight_experience * structured["experience"].score
        + settings.weight_education * structured["education"].score
        + settings.weight_preferred_skills * structured["preferred_skills"].score
    )

    breakdown = MatchBreakdown(
        required_skills=structured["required_skills"],
        preferred_skills=structured["preferred_skills"],
        semantic_similarity=tfidf_score,
        experience=structured["experience"],
        education=structured["education"],
    )

    return MatchResult(
        overall_score=round(overall, 4),
        breakdown=breakdown,
        summary=_generate_summary(overall, breakdown),
    )


def score_embedding_only(
    resume_text: str,
    jd_text: str,
    resume_entities: ResumeEntities,
    jd_entities: JobDescriptionEntities,
) -> MatchResult:
    settings = get_settings()

    emb_score = score_embedding(resume_text, jd_text)
    structured = score_structured(resume_entities, jd_entities)

    overall = (
        settings.weight_required_skills * structured["required_skills"].score
        + settings.weight_semantic * emb_score
        + settings.weight_experience * structured["experience"].score
        + settings.weight_education * structured["education"].score
        + settings.weight_preferred_skills * structured["preferred_skills"].score
    )

    breakdown = MatchBreakdown(
        required_skills=structured["required_skills"],
        preferred_skills=structured["preferred_skills"],
        semantic_similarity=emb_score,
        experience=structured["experience"],
        education=structured["education"],
    )

    return MatchResult(
        overall_score=round(overall, 4),
        breakdown=breakdown,
        summary=_generate_summary(overall, breakdown),
    )
