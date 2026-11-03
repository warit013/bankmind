from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.rag.embeddings import embed
from app.routers import ask, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    embed(["warmup"])  # โหลด bge-m3 ตอนเริ่ม เพื่อให้คำถามแรกไม่ช้า
    yield


app = FastAPI(title="BankMind", version="0.1.0", lifespan=lifespan)
app.include_router(health.router)
app.include_router(ask.router)