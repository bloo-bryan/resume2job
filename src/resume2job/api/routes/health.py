from fastapi import APIRouter

from resume2job.api.schemas import HealthResponse

router = APIRouter()


@router.get("/api/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    models_loaded = True
    try:
        from resume2job.extraction.ner import build_nlp_pipeline

        build_nlp_pipeline()
    except Exception:
        models_loaded = False

    qdrant_connected = False
    try:
        from qdrant_client import QdrantClient

        from resume2job.config import get_settings

        settings = get_settings()
        client = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port, timeout=2)
        client.get_collections()
        qdrant_connected = True
    except Exception:
        pass

    status = "healthy" if models_loaded else "unhealthy"
    return HealthResponse(
        status=status, models_loaded=models_loaded, qdrant_connected=qdrant_connected
    )
