from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Experience:
    source: str
    content: str
    timestamp: float
    modality: str
