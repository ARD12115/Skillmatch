import logging
import os
from functools import lru_cache

from requests.exceptions import RequestException
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)
DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def _load_embedding_model(model_name: str):
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(model_name)


def semantic_similarity(
    a: str, b: str, use_embeddings: bool | None = None
) -> tuple[float, str]:
    """Compare two texts with embeddings when available, otherwise TF-IDF."""
    if not a.strip() or not b.strip():
        return 0.0, "tfidf"
    if use_embeddings is None:
        use_embeddings = os.getenv("USE_EMBEDDINGS", "true").casefold() not in {
            "0",
            "false",
            "no",
        }

    if use_embeddings:
        model_name = os.getenv("EMBEDDING_MODEL", DEFAULT_MODEL)
        try:
            embeddings = _load_embedding_model(model_name).encode([a, b])
            score = float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])
            return min(1.0, max(0.0, score)), "embeddings"
        except (
            ImportError,
            OSError,
            RequestException,
            RuntimeError,
            ValueError,
        ) as exc:
            logger.warning(
                "Embedding similarity unavailable (%s); using TF-IDF fallback.",
                type(exc).__name__,
            )

    try:
        matrix = TfidfVectorizer(ngram_range=(1, 2)).fit_transform([a, b])
        score = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
    except ValueError:
        score = 0.0
    return min(1.0, max(0.0, score)), "tfidf"
