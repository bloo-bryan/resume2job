from pydantic import BaseModel


class MatchRequest(BaseModel):
    resume_text: str
    jd_text: str
    algorithm: str = "hybrid"
    weights: dict[str, float] | None = None


class CompareRequest(BaseModel):
    resume_text: str
    jd_text: str
    weights: dict[str, float] | None = None


class HealthResponse(BaseModel):
    status: str
    models_loaded: bool
    qdrant_connected: bool


class AlgorithmMetricsResponse(BaseModel):
    ndcg_at_5: float
    mrr: float
    precision_at_3: float


class EvaluationResponse(BaseModel):
    test_set_size: int
    metrics: dict[str, AlgorithmMetricsResponse]
