from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Intention:
    description: str
    status: str = "PENDING"
    goal_id: str | None = None
    id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self) -> None:
        self.description = self.description.strip()

        if not self.description:
            raise ValueError("Intention description cannot be empty")

        if self.status not in {"PENDING", "ACTIVE", "COMPLETED"}:
            raise ValueError(
                f"Invalid intention status: {self.status}"
            )

    def activate(self) -> None:
        self.status = "ACTIVE"

    def complete(self) -> None:
        self.status = "COMPLETED"
