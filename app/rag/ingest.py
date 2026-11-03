import sys
from pathlib import Path

from pypdf import PdfReader

from app.rag.chunking import split_text
from app.rag.db import get_conn, init_db
from app.rag.embeddings import embed


def read_pages(path: Path) -> list[tuple[int, str]]:
    if path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))
        return [(i + 1, p.extract_text() or "") for i, p in enumerate(reader.pages)]
    return [(1, path.read_text(encoding="utf-8"))]


def ingest_file(path: Path) -> int:
    pieces: list[tuple[int, str]] = []
    for page, text in read_pages(path):
        pieces += [(page, c) for c in split_text(text)]
    if not pieces:
        print(f"skip (no text): {path.name}")
        return 0

    vectors = embed([c for _, c in pieces])
    with get_conn() as conn:
        conn.execute("DELETE FROM documents WHERE source = %s", (path.name,))
        doc_id = conn.execute(
            "INSERT INTO documents (source) VALUES (%s) RETURNING id", (path.name,)
        ).fetchone()[0]
        for i, ((page, content), vec) in enumerate(zip(pieces, vectors)):
            conn.execute(
                "INSERT INTO chunks (document_id, chunk_index, page, content, embedding)"
                " VALUES (%s, %s, %s, %s, %s)",
                (doc_id, i, page, content, vec),
            )
    print(f"ingested {path.name}: {len(pieces)} chunks")
    return len(pieces)


if __name__ == "__main__":
    init_db()
    folder = Path(sys.argv[1] if len(sys.argv) > 1 else "data/raw")
    files = [p for p in folder.iterdir() if p.suffix.lower() in {".pdf", ".txt", ".md"}]
    if not files:
        print(f"ไม่พบไฟล์ใน {folder}")
    for f in files:
        ingest_file(f)