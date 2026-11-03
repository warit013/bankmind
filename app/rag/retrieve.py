from pgvector import Vector

from app.rag.db import get_conn
from app.rag.embeddings import embed


def retrieve(question: str, k: int = 5) -> list[dict]:
    qvec = Vector(embed([question])[0])
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT d.source, c.page, c.content, 1 - (c.embedding <=> %s) AS score
            FROM chunks c JOIN documents d ON d.id = c.document_id
            ORDER BY c.embedding <=> %s
            LIMIT %s
            """,
            (qvec, qvec, k),
        ).fetchall()
    return [
        {"source": r[0], "page": r[1], "content": r[2], "score": round(float(r[3]), 4)}
        for r in rows
    ]