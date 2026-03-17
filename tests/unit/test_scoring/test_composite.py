from resume2job.models import (
    EducationBreakdown,
    ExperienceBreakdown,
    MatchBreakdown,
    SkillsBreakdown,
)
from resume2job.scoring.composite import _generate_summary, score_hybrid


class TestGenerateSummary:
    def test_strong_match(self) -> None:
        breakdown = MatchBreakdown(
            required_skills=SkillsBreakdown(score=1.0, matched=["python"], missing=[]),
            preferred_skills=SkillsBreakdown(score=1.0, matched=[], missing=[]),
            semantic_similarity=0.9,
            experience=ExperienceBreakdown(score=1.0, required=3, detected=5),
            education=EducationBreakdown(score=1.0, required="B.S.", detected="M.S."),
        )
        summary = _generate_summary(0.85, breakdown)
        assert "Strong match (85%)" in summary
        assert "All 1 required skills matched" in summary

    def test_weak_match_with_missing_skills(self) -> None:
        breakdown = MatchBreakdown(
            required_skills=SkillsBreakdown(
                score=0.5, matched=["python"], missing=["kubernetes", "spark"]
            ),
            preferred_skills=SkillsBreakdown(score=0.0, matched=[], missing=["docker"]),
            semantic_similarity=0.3,
            experience=ExperienceBreakdown(score=0.5, required=5, detected=2),
            education=EducationBreakdown(score=1.0, required="B.S.", detected="B.S."),
        )
        summary = _generate_summary(0.35, breakdown)
        assert "Weak match (35%)" in summary
        assert "Missing 2" in summary
        assert "kubernetes" in summary


class TestScoreHybrid:
    def test_returns_match_result(
        self, sample_resume_text: str, sample_jd_text: str, nlp_pipeline
    ) -> None:
        from resume2job.extraction import extract_jd_entities, extract_resume_entities

        resume_ent = extract_resume_entities(sample_resume_text, nlp_pipeline)
        jd_ent = extract_jd_entities(sample_jd_text, nlp_pipeline)
        result = score_hybrid(sample_resume_text, sample_jd_text, resume_ent, jd_ent)

        assert 0.0 <= result.overall_score <= 1.0
        assert result.summary
        assert result.breakdown.required_skills.score >= 0.0
        assert isinstance(result.breakdown.semantic_similarity, float)

    def test_perfect_self_match_scores_high(self, sample_resume_text: str, nlp_pipeline) -> None:
        from resume2job.extraction import extract_jd_entities, extract_resume_entities

        resume_ent = extract_resume_entities(sample_resume_text, nlp_pipeline)
        jd_ent = extract_jd_entities(sample_resume_text, nlp_pipeline)
        result = score_hybrid(sample_resume_text, sample_resume_text, resume_ent, jd_ent)

        assert result.overall_score > 0.5, (
            f"Self-match should score high, got {result.overall_score}"
        )
