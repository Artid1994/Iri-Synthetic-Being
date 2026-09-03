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


class WebResearch:
    def __init__(
        self,
        search_url: str = "https://duckduckgo.com/search?q=",
        timeout: float = 10.0,
    ) -> None:
        self.search_url = search_url
        self.timeout = timeout

    def search(self, topic: str) -> ResearchResult:
        topic = topic.strip()

        if not topic:
            raise ValueError("research topic cannot be empty")

        url = self.search_url + quote(topic)

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

        return ResearchResult(
            topic=topic,
            source=url,
            content=clean_content,
        )
