import logging

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine

logger = logging.getLogger(__name__)

DOMAIN_STOP_WORDS: list[str] = [
    "resume",
    "curriculum",
    "vitae",
    "experience",
    "responsible",
    "responsibilities",
    "duty",
    "duties",
    "job",
    "description",
    "position",
    "candidate",
    "apply",
    "application",
]


def _build_stop_words() -> list[str]:
    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

    return list(ENGLISH_STOP_WORDS | set(DOMAIN_STOP_WORDS))


def score_tfidf(resume_text: str, jd_text: str) -> float:
    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words=_build_stop_words(),
        max_features=5000,
    )
    tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
    sim = sklearn_cosine(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return float(sim[0][0])
