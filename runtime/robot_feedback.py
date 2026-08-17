from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RobotFeedback:
    success: bool
    action: str
    value: object
    error: str | None = None
