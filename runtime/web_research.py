from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote
import re
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class ResearchResult:
    topic: str
    source: str
    content: str
    timestamp: float | None = None


class WebResearch:
    def __init__(
        self,
        search_url: str = "https://duckduckgo.com/search?q=",
        timeout: float = 10.0,
    ) -> None:
        self.search_url = search_url
        self.timeout = timeout

    @staticmethod
    def normalize_query(topic: str) -> str:
        text = topic.strip()
        if not text:
            return ""

        # Strip operational task prefixes deterministically (case-insensitive)
        prefixes = [
            r"^research\s+missing\s+knowledge\s+(?:for|about):\s*",
            r"^research\s+missing\s+knowledge:\s*",
            r"^research\s+missing\s+knowledge\s*",
            r"^investigate\s+failure\s+of:\s*",
            r"^investigate\s+failure\s+of\s*",
            r"^investigate\s+previous\s+failure:\s*",
            r"^investigate\s+previous\s+failure\s*",
            r"^research\s+for:\s*",
            r"^research:\s*",
            r"^research\s+",
            r"^investigate:\s*",
            r"^investigate\s+",
        ]
        for pattern in prefixes:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                stripped = text[match.end():].strip()
                if stripped:
                    text = stripped
                    break

        # Remove extraneous enclosing quotes if present
        if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
            text = text[1:-1].strip()

        return text

    def search(self, topic: str) -> ResearchResult:
        raw_topic = topic.strip()
        if not raw_topic:
            raise ValueError("research topic cannot be empty")

        clean_query = self.normalize_query(raw_topic) or raw_topic
        url = self.search_url + quote(clean_query)

        request = Request(
            url,
            headers={
                "User-Agent": "TTF-Learning-Agent/0.1",
            },
        )

        with urlopen(request, timeout=self.timeout) as response:
            content = response.read().decode(
                "utf-8",
                errors="replace",
            )

        # --- HTML Stripper Integration v2 (High-Definition) ---
        # 1. ลบโค้ด script และ style รวมถึงเนื้อหาภายในทั้งหมด
        clean_content = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", content, flags=re.DOTALL | re.IGNORECASE)
        # 2. ลบเศษรหัสขยะ CSS หรือโค้ดที่อยู่ในวงเล็บปีกกา {...} ทั้งหมดออกไป
        clean_content = re.sub(r"\{[^}]*\}", " ", clean_content)
        # 3. ลบแท็ก HTML ที่เหลือทั้งหมดออกไป
        clean_content = re.sub(r"<[^>]+>", " ", clean_content)
        # 4. ล้างคำเฉพาะที่เกี่ยวกับกลไกบล็อกบอทของ Search Engine
        clean_content = re.sub(r"(window\.google|display:\s*none)", " ", clean_content, flags=re.IGNORECASE)
        # 5. จัดการระยะเว้นวรรคและบรรทัดให้เหลือแต่ Plain Text สะอาดๆ
        clean_content = re.sub(r"\s+", " ", clean_content).strip()
        # 6. จำกัดความยาวข้อความเนื้อหาเน้นๆ ส่งต่อให้โมเดลประมวลผลต่อได้ง่าย
        clean_content = clean_content[:2500]

        import time
        return ResearchResult(
            topic=clean_query,
            source=url,
            content=clean_content,
            timestamp=time.time(),
        )
