import logging

from fastapi import APIRouter, HTTPException

from resume2job.api.schemas import AlgorithmMetricsResponse, EvaluationResponse
from resume2job.evaluation import run_benchmark

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/evaluation", response_model=EvaluationResponse)
def evaluation_endpoint() -> EvaluationResponse:
    try:
        result = run_benchmark()
    except FileNotFoundError as exc:
        logger.error("Evaluation test set not found: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="Evaluation test set not found (labels.json missing)",
        ) from exc
    except RuntimeError as exc:
        logger.error("Evaluation benchmark failed: %s", exc)
        raise HTTPException(
            status_code=500, detail=str(exc)
        ) from exc
    metrics = {}
    for algo_name in ("tfidf", "embedding", "hybrid"):
        algo_metrics = getattr(result, algo_name)
        metrics[algo_name] = AlgorithmMetricsResponse(
            ndcg_at_5=algo_metrics.ndcg_at_5,
            mrr=algo_metrics.mrr,
            precision_at_3=algo_metrics.precision_at_3,
        )
    return EvaluationResponse(test_set_size=result.test_set_size, metrics=metrics)
