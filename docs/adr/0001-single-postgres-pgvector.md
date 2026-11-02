# ADR-0001: ใช้ PostgreSQL + pgvector เป็นฐานข้อมูลเดียว

## Status
Accepted

## Context
ต้องเก็บข้อมูลธุรกรรมของแอป (เรื่องร้องเรียน, audit log) และ vector embeddings สำหรับ RAG

## Decision
ใช้ PostgreSQL + pgvector ตัวเดียว แทนแยก vector DB

## Consequences
+ ดูแลง่าย ทรานแซกชันและ audit รวมที่เดียว deploy ถูก
+ ย้ายไป Azure Database for PostgreSQL ได้ตรง ๆ
- ถ้า vector เกินหลักล้านระเบียนอาจต้องพิจารณา Azure AI Search