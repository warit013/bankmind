from functools import lru_cache

from sentence_transformers import SentenceTransformer


@lru_cache(maxsize=1)
def _model() -> SentenceTransformer:
    return SentenceTransformer("BAAI/bge-m3")


def embed(texts: list[str]) -> list[list[float]]:
    vecs = _model().encode(texts, batch_size=16, normalize_embeddings=True)
    return vecs.tolist()