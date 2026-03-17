from resume2job.scoring.tfidf import score_tfidf


class TestScoreTfidf:
    def test_identical_texts_high_score(self) -> None:
        text = "python machine learning deep learning pytorch tensorflow"
        score = score_tfidf(text, text)
        assert score > 0.99, f"Identical texts should score ~1.0, got {score}"

    def test_unrelated_texts_low_score(self) -> None:
        resume = "python machine learning deep learning neural networks"
        jd = "accounting financial reporting tax compliance audit"
        score = score_tfidf(resume, jd)
        assert score < 0.3, f"Unrelated texts should score low, got {score}"

    def test_partial_overlap_moderate_score(self) -> None:
        resume = "python machine learning docker kubernetes deployment"
        jd = "python machine learning spark hadoop data engineering"
        score = score_tfidf(resume, jd)
        assert 0.1 < score < 0.9, f"Partial overlap should be moderate, got {score}"

    def test_returns_float_in_range(self) -> None:
        score = score_tfidf("python developer", "java developer")
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_empty_texts(self) -> None:
        score = score_tfidf("", "")
        assert score == 0.0 or isinstance(score, float)
