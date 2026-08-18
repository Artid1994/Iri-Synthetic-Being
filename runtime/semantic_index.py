from __future__ import annotations


class SemanticIndex:
    """ดัชนี membership สำหรับ Semantic Memory โดยไม่เปลี่ยน storage เดิม"""

    def __init__(self) -> None:
        self._values: set[str] = set()

    def add(self, knowledge: str) -> None:
        self._values.add(knowledge)

    def contains(self, knowledge: str) -> bool:
        return knowledge in self._values

    def __contains__(self, knowledge: str) -> bool:
        return knowledge in self._values

    def __len__(self) -> int:
        return len(self._values)

    def snapshot(self) -> set[str]:
        return set(self._values)
