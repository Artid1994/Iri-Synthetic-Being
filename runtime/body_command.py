from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BodyCommand:
    action: str
    value: object | None = None
