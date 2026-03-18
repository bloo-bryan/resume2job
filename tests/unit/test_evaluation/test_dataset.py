from resume2job.evaluation.dataset import load_test_set, load_texts


class TestLoadTestSet:
    def test_loads_pairs(self) -> None:
        test_set = load_test_set()
        assert len(test_set.pairs) >= 20
        for pair in test_set.pairs:
            assert pair.relevance in (0, 1, 2, 3)
            assert pair.jd_file.startswith("job_descriptions/")
            assert pair.resume_file.startswith("resumes/")


class TestLoadTexts:
    def test_loads_text_files(self) -> None:
        test_set = load_test_set()
        resume_text, jd_text = load_texts(test_set.pairs[0])
        assert len(resume_text) > 100
        assert len(jd_text) > 100
