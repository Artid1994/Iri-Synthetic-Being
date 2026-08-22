from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Goal:
    description: str
    priority: int = 0
    status: str = "ACTIVE"
    id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self) -> None:
        self.description = self.description.strip()

        if not self.description:
            raise ValueError("Goal description cannot be empty")

        if self.status not in {"ACTIVE", "COMPLETED", "PAUSED"}:
            raise ValueError(f"Invalid goal status: {self.status}")

    def complete(self) -> None:
        self.status = "COMPLETED"

    def pause(self) -> None:
        self.status = "PAUSED"
