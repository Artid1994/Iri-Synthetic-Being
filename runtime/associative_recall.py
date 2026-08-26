from __future__ import annotations

import re

from runtime.memory import Memory


class AssociativeRecall:
    """Minimal associative recall with lightweight contextual matching."""

    _QUESTION_SUFFIXES = (
        "หรือไม่",
        "อะไร",
        "ไหม",
        "มั้ย",
        "หรือ",
    )

    def __init__(self, memory: Memory) -> None:
        self.memory = memory

    def remember(self, key: str, value: str) -> None:
        key = key.strip()
        value = value.strip()

        if not key or not value:
            return

        self.memory.associate(key, value)

    def recall(self, key: str) -> list[str]:
        key = key.strip()

        if not key:
            return []

        exact = self.memory.associations(key)
        if exact:
            return exact

        query = self._normalize_query(key)

        if not query:
            return []

        results: list[str] = []

        for experience in reversed(self.memory.state.episodic):
            normalized = self._normalize_query(experience)

            if query in normalized or normalized.startswith(query):
                results.append(experience)

        return results[:3]

    @classmethod
    def _normalize_query(cls, text: str) -> str:
        text = text.strip().lower()

        text = re.sub(
            r"[?!.,:;\"'()\[\]{}]",
            "",
            text,
        )

        for suffix in cls._QUESTION_SUFFIXES:
            if text.endswith(suffix):
                text = text[:-len(suffix)].strip()
                break

        text = text.replace("สีโปรดของฉัน", "ฉันชอบสี")
        text = text.replace("คือ", "")

        return text.strip()
