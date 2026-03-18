import math


def ndcg_at_k(relevances: list[float], k: int) -> float:
    actual = relevances[: min(k, len(relevances))]

    dcg = sum(rel / math.log2(i + 2) for i, rel in enumerate(actual))

    ideal = sorted(relevances, reverse=True)[: min(k, len(relevances))]
    idcg = sum(rel / math.log2(i + 2) for i, rel in enumerate(ideal))

    if idcg == 0:
        return 0.0

    return dcg / idcg


def mrr(relevances: list[float]) -> float:
    for i, rel in enumerate(relevances):
        if rel > 0:
            return 1.0 / (i + 1)
    return 0.0


def precision_at_k(relevances: list[float], k: int) -> float:
    actual = relevances[: min(k, len(relevances))]
    if not actual:
        return 0.0
    return sum(1 for rel in actual if rel > 0) / len(actual)
