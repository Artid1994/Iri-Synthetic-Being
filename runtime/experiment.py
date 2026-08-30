from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Experiment:
    hypothesis: str
    parameters: dict[str, Any]
    objective: str


@dataclass(frozen=True)
class ExperimentResult:
    metrics: dict[str, float]
    status: str
    error: str | None = None
