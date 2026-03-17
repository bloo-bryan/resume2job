import pytest

from resume2job.scoring.embedding import score_embedding


@pytest.mark.slow
class TestScoreEmbedding:
    def test_identical_texts_high_score(self) -> None:
        text = "senior machine learning engineer with python and pytorch experience"
        score = score_embedding(text, text)
        assert score > 0.99, f"Identical texts should score ~1.0, got {score}"

    def test_similar_texts_high_score(self) -> None:
        resume = "experienced python developer specializing in machine learning and deep learning"
        jd = "looking for a python engineer with machine learning and deep learning skills"
        score = score_embedding(resume, jd)
        assert score > 0.7, f"Similar texts should score high, got {score}"

    def test_unrelated_texts_lower_score(self) -> None:
        resume = "python machine learning deep learning neural networks pytorch"
        jd = "accounting financial reporting tax compliance audit procedures"
        score = score_embedding(resume, jd)
        assert score < 0.5, f"Unrelated texts should score lower, got {score}"

    def test_returns_float_in_range(self) -> None:
        score = score_embedding("python developer", "java developer")
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
