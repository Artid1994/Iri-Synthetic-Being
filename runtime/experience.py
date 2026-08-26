from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Experience:
    source: str
    content: str
    timestamp: float
    modality: str
    salience: float = 0.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.salience <= 1.0:
            raise ValueError("Experience salience must be between 0.0 and 1.0")
