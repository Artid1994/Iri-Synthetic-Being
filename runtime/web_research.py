from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class ResearchResult:
    topic: str
    source: str
    content: str


class WebResearch:
    def __init__(
        self,
        search_url: str = "https://www.google.com/search?q=",
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

        return ResearchResult(
            topic=topic,
            source=url,
            content=content,
        )
