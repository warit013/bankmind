import json
import random
import sys

from app.llm import chat
from app.rag.db import get_conn

N = int(sys.argv[1]) if len(sys.argv) > 1 else 20
random.seed(42)

with get_conn() as conn:
    rows = conn.execute(
        "SELECT d.source, c.page, c.content FROM chunks c "
        "JOIN documents d ON d.id=c.document_id WHERE length(c.content) > 300"
    ).fetchall()

picked = random.sample(rows, min(N, len(rows)))
out = []
for source, page, content in picked:
    q = chat([
        {"role": "system", "content": "สร้างคำถามภาษาไทย 1 ข้อ ที่ตอบได้จากข้อความที่ให้เท่านั้น "
         "ตอบเฉพาะตัวคำถาม ไม่ต้องอธิบาย และห้ามอ้างถึง 'ข้อความ' หรือ 'เอกสารนี้'"},
        {"role": "user", "content": content},
    ]).strip().splitlines()[0]
    out.append({"question": q, "source": source, "page": page})
    print(page, q)

with open("eval/questions_auto.jsonl", "w", encoding="utf-8") as f:
    for o in out:
        f.write(json.dumps(o, ensure_ascii=False) + "\n")
print(f"saved {len(out)} questions")