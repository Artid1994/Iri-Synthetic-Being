from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ExecutionResult:
    success: bool
    action: str
    value: Any
    error: str | None = None
