from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Teaching:
    content: str
    status: str = "PENDING"
    id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self) -> None:
        self.content = self.content.strip()

        if not self.content:
            raise ValueError("Teaching content cannot be empty")

        if self.status not in {"PENDING", "ACCEPTED", "REJECTED"}:
            raise ValueError(
                f"Invalid teaching status: {self.status}"
            )

    def accept(self) -> None:
        self.status = "ACCEPTED"

    def reject(self) -> None:
        self.status = "REJECTED"
