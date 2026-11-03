# ADR-0002: โมเดลแบบ local-first และสลับ provider ได้

## Status
Accepted

## Context
โดเมนธนาคารมีข้อมูลอ่อนไหว จึงต้องการให้ข้อมูลไม่ออกนอกเครื่องในช่วงพัฒนา และต้องย้ายไป Azure OpenAI ได้ภายหลัง

## Decision
- Embedding: BAAI/bge-m3 รันในเครื่อง (รองรับภาษาไทย, 1024 มิติ)
- LLM: Ollama (qwen2.5) เป็นค่าเริ่มต้น สลับเป็น OpenAI/Azure OpenAI ผ่าน LLM_PROVIDER
- ทุกการเรียก LLM ผ่านฟังก์ชัน chat() จุดเดียวใน app/llm.py

## Consequences
+ ข้อมูลไม่ออกนอกเครื่อง ไม่มีค่า API ช่วงพัฒนา
+ เปลี่ยน provider โดยแก้ config ไม่ต้องแก้ logic
- คุณภาพภาษาไทยของโมเดลโลคอลต่ำกว่าโมเดลคลาวด์ขนาดใหญ่ ต้องวัดด้วย eval