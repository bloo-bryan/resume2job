import logging
from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

from resume2job.config import get_settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _load_model() -> SentenceTransformer:
    settings = get_settings()
    logger.info("Loading sentence-transformer model: %s", settings.sentence_transformer_model)
    return SentenceTransformer(
        settings.sentence_transformer_model,
        cache_folder=str(settings.model_cache_dir),
    )


def score_embedding(resume_text: str, jd_text: str) -> float:
    model = _load_model()
    embeddings = model.encode([resume_text, jd_text], convert_to_numpy=True)
    sim = np.dot(embeddings[0], embeddings[1]) / (
        np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
    )
    return float(np.clip(sim, 0.0, 1.0))
