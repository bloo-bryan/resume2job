from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = {"env_prefix": "R2J_"}

    skills_csv_path: Path = PROJECT_ROOT / "data" / "skills" / "skills.csv"
    spacy_model: str = "en_core_web_lg"
    sentence_transformer_model: str = "all-MiniLM-L6-v2"
    model_cache_dir: Path = PROJECT_ROOT / "models"
    max_upload_size_mb: int = 10
    environment: str = "dev"
    log_level: str = "INFO"

    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "resumes"

    # Composite ranker weights (PRD F6) — must sum to 1.0
    weight_required_skills: float = 0.30
    weight_semantic: float = 0.40
    weight_experience: float = 0.15
    weight_education: float = 0.10
    weight_preferred_skills: float = 0.05

    # Hybrid semantic blend weights — must sum to 1.0
    hybrid_tfidf_weight: float = 0.35
    hybrid_embedding_weight: float = 0.65


@lru_cache
def get_settings() -> Settings:
    return Settings()
