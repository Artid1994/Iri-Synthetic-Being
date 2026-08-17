from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HumanData:
    biography: object | None = None
    conversation: object | None = None
    writing_style: object | None = None
    preferences: object | None = None
    experiences: object | None = None
    values: object | None = None
    beliefs: object | None = None
    memories: object | None = None
    decision_patterns: object | None = None
    emotional_associations: object | None = None
