import json
import re
import statistics
import sys
import time
from pathlib import Path

from app.llm import chat
from app.rag.retrieve import retrieve
from app.routers.ask import SYSTEM_PROMPT
from app.config import settings

REFUSAL = "ไม่พบข้อมูล"


def load(path):
    p = Path(path)
    if not p.exists():
        return []
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def answer(q):
    hits = retrieve(q, settings.top_k)
    ctx = "\n\n".join(
        f"[{i}] (ไฟล์: {h['source']}, หน้า {h['page']})\n{h['content']}" for i, h in enumerate(hits, 1)
    )
    t = time.time()
    a = chat([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"บริบท:\n{ctx}\n\nคำถาม: {q}"},
    ])
    return a, hits, time.time() - t


def pct(x, n):
    return f"{100 * x / n:.0f}% ({x}/{n})" if n else "n/a"


# ---- B: auto questions -> retrieval hit rate
auto = load("eval/questions_auto.jsonl")
hit_k, hit_1 = 0, 0
for item in auto:
    hits = retrieve(item["question"], settings.top_k)
    pages = [h["page"] for h in hits]
    hit_k += item["page"] in pages
    hit_1 += bool(pages) and pages[0] == item["page"]

# ---- A: manual questions
manual = load("eval/questions_manual.jsonl")
ans_total = ans_kw = ans_kw_n = ans_cite = ans_page = ans_page_n = 0
un_total = un_refused = 0
lat = []
for item in manual:
    a, hits, sec = answer(item["question"])
    lat.append(sec)
    if item["type"] == "unanswerable":
        un_total += 1
        un_refused += REFUSAL in a
        continue
    ans_total += 1
    ans_cite += bool(re.search(r"\[\d+\]", a))
    if item["expected_keywords"]:
        ans_kw_n += 1
        ans_kw += all(k in a for k in item["expected_keywords"])
    if item["expected_pages"]:
        ans_page_n += 1
        ans_page += any(h["page"] in item["expected_pages"] for h in hits)

print("=" * 50)
print(f"model: {settings.llm_model} | top_k: {settings.top_k}")
print(f"[B] Retrieval hit@{settings.top_k}: {pct(hit_k, len(auto))}   hit@1: {pct(hit_1, len(auto))}")
print(f"[A] Citation rate:        {pct(ans_cite, ans_total)}")
print(f"[A] Keyword accuracy:     {pct(ans_kw, ans_kw_n)}  (เฉพาะข้อที่กรอกเฉลยแล้ว)")
print(f"[A] Page hit (manual):    {pct(ans_page, ans_page_n)}  (เฉพาะข้อที่กรอกเฉลยแล้ว)")
print(f"[A] Refusal accuracy:     {pct(un_refused, un_total)}  (คำถามนอกเรื่องที่ปฏิเสธถูก)")
if lat:
    print(f"Latency avg {statistics.mean(lat):.1f}s | max {max(lat):.1f}s")
print("=" * 50)