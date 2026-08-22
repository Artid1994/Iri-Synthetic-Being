from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyEvent:
    action: str
    value: object | None
    reason: str
