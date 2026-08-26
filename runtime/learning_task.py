from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class LearningTask:
    topic: str
    status: str = "PENDING"
    id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self) -> None:
        self.topic = self.topic.strip()

        if not self.topic:
            raise ValueError("Learning task topic cannot be empty")

        if self.status not in {"PENDING", "ACTIVE", "COMPLETED"}:
            raise ValueError(
                f"Invalid learning task status: {self.status}"
            )

    def start(self) -> None:
        if self.status != "PENDING":
            raise ValueError(
                f"Cannot start learning task from status: {self.status}"
            )

        self.status = "ACTIVE"

    def complete(self) -> None:
        if self.status != "ACTIVE":
            raise ValueError(
                f"Cannot complete learning task from status: {self.status}"
            )

        self.status = "COMPLETED"
