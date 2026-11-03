def split_text(text: str, size: int = 800, overlap: int = 120) -> list[str]:
    """แบ่งข้อความเป็น chunk ตามขนาดตัวอักษร โดยพยายามตัดที่ช่องว่าง
    (ภาษาไทยไม่มีช่องว่างระหว่างคำ จึงใช้ขนาดตัวอักษรเป็นหลัก)"""
    text = " ".join(text.split())
    chunks, start = [], 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            cut = text.rfind(" ", start + size // 2, end)
            if cut != -1:
                end = cut
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks