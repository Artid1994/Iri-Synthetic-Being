from __future__ import annotations


class RecallIndex:
    """ดัชนีค้นหา exact-match สำหรับ Episodic Memory โดยรักษาลำดับ Memory เดิม"""

    def __init__(self) -> None:
        self._latest: dict[str, int] = {}

    def add(self, experience: str, position: int) -> None:
        self._latest[experience] = position

    def find_latest(self, experience: str) -> int | None:
        return self._latest.get(experience)

    def rebuild(self, experiences: list[str]) -> None:
        self._latest.clear()

        for position, experience in enumerate(experiences):
            self._latest[experience] = position

    def __len__(self) -> int:
        return len(self._latest)

    def snapshot(self) -> dict[str, int]:
        return dict(self._latest)
