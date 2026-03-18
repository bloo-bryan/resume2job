from resume2job.evaluation.metrics import mrr, ndcg_at_k, precision_at_k


class TestNDCG:
    def test_perfect_ranking(self) -> None:
        assert ndcg_at_k([3, 2, 1, 0], k=4) == 1.0

    def test_reversed_ranking(self) -> None:
        assert ndcg_at_k([0, 1, 2, 3], k=4) < 1.0

    def test_single_relevant(self) -> None:
        assert ndcg_at_k([1], k=1) == 1.0

    def test_all_zeros(self) -> None:
        assert ndcg_at_k([0, 0, 0], k=3) == 0.0

    def test_k_larger_than_list(self) -> None:
        result = ndcg_at_k([3, 2], k=5)
        assert 0.0 <= result <= 1.0


class TestMRR:
    def test_first_is_relevant(self) -> None:
        assert mrr([3, 0, 0]) == 1.0

    def test_second_is_relevant(self) -> None:
        assert mrr([0, 1, 0]) == 0.5

    def test_none_relevant(self) -> None:
        assert mrr([0, 0, 0]) == 0.0


class TestPrecisionAtK:
    def test_all_relevant(self) -> None:
        assert precision_at_k([3, 2, 1], k=3) == 1.0

    def test_none_relevant(self) -> None:
        assert precision_at_k([0, 0, 0], k=3) == 0.0

    def test_half_relevant(self) -> None:
        assert precision_at_k([1, 0, 1, 0], k=4) == 0.5
