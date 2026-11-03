from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.config import settings
from app.llm import chat
from app.rag.retrieve import retrieve

router = APIRouter(tags=["rag"])

SYSTEM_PROMPT = (
    "คุณคือผู้ช่วยตอบคำถามเกี่ยวกับกฎหมายและนโยบายภายในองค์กร "
    "ตอบเป็นภาษาไทยโดยอ้างอิงจาก 'บริบท' ที่ให้มาเท่านั้น "
    "ระบุหมายเลขแหล่งอ้างอิงในรูปแบบ [1], [2] ท้ายประโยคที่ใช้ข้อมูลนั้น "
    "หากบริบทไม่มีข้อมูลเพียงพอ ให้ตอบว่า 'ไม่พบข้อมูลในเอกสารที่มี' "
    "ห้ามเดาหรือใช้ความรู้นอกเหนือจากบริบท"
)


class AskRequest(BaseModel):
    question: str = Field(min_length=3)
    top_k: int | None = None


@router.post("/ask")
def ask(req: AskRequest):
    hits = retrieve(req.question, req.top_k or settings.top_k)
    context = "\n\n".join(
        f"[{i}] (ไฟล์: {h['source']}, หน้า {h['page']})\n{h['content']}"
        for i, h in enumerate(hits, 1)
    )
    answer = chat(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"บริบท:\n{context}\n\nคำถาม: {req.question}"},
        ]
    )
    return {
        "answer": answer,
        "sources": [
            {"ref": i, "source": h["source"], "page": h["page"], "score": h["score"]}
            for i, h in enumerate(hits, 1)
        ],
    }