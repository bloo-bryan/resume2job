from fastapi import APIRouter

from resume2job.api.schemas import AlgorithmMetricsResponse, EvaluationResponse
from resume2job.evaluation import run_benchmark

router = APIRouter()


@router.get("/api/evaluation", response_model=EvaluationResponse)
def evaluation_endpoint() -> EvaluationResponse:
    result = run_benchmark()
    metrics = {}
    for algo_name in ("tfidf", "embedding", "hybrid"):
        algo_metrics = getattr(result, algo_name)
        metrics[algo_name] = AlgorithmMetricsResponse(
            ndcg_at_5=algo_metrics.ndcg_at_5,
            mrr=algo_metrics.mrr,
            precision_at_3=algo_metrics.precision_at_3,
        )
    return EvaluationResponse(test_set_size=result.test_set_size, metrics=metrics)
