from __future__ import annotations

from pathlib import Path

from runtime.ollama_inference import OllamaInference


class CodeReviewer:
    def __init__(self) -> None:
        self.ai = OllamaInference(
            model="qwen2.5:1.5b",
            timeout=120,
        )

    def review(self, path: str) -> str:
        file = Path(path)
        code = file.read_text(encoding="utf-8")

        prompt = f"""ตรวจสอบโค้ด Python นี้
ไฟล์: {file}

ระบุเฉพาะ:
1. bug ที่พบ
2. ปัญหาที่อาจเกิดขึ้น
3. ข้อเสนอแนะสั้น ๆ

ห้ามแก้โค้ด
ห้ามสร้างคำสั่ง shell

CODE:
{code}
"""

        return self.ai(prompt)
