from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Role:
    """Represents the functional role/capacity of the agent (What am I doing?).

    Explicitly distinct from:
    - Identity (Who am I?)
    - Purpose (Why am I doing it?)
    - Goal/Intention (What concrete objectives am I pursuing?)
    - Safety Boundary (What am I allowed to do?)
    """

    name: str
    description: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", self.name.strip())
        object.__setattr__(self, "description", self.description.strip())
        if not self.name:
            raise ValueError("Role name cannot be empty")


@dataclass(frozen=True)
class Purpose:
    """Represents the declared foundational reason or orientation of the agent (Why am I doing it?).

    Explicitly distinct from:
    - Identity (Who am I?)
    - Role (What am I doing?)
    - Goal (Specific concrete state to achieve)
    - Safety Boundary (Constraint envelope)
    """

    declaration: str
    rationale: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "declaration", self.declaration.strip())
        object.__setattr__(self, "rationale", self.rationale.strip())
        if not self.declaration:
            raise ValueError("Purpose declaration cannot be empty")


@dataclass(frozen=True)
class SafetyBoundary:
    """Defines the operational constraints and boundary envelope (What am I allowed to do?).

    Explicitly distinct from:
    - Identity (Who am I?)
    - Role (What am I doing?)
    - Purpose (Why am I doing it?)
    - Goal / Intention (Objectives pursued)
    """

    allowed_actions: tuple[str, ...] = ("move", "respond")
    max_rate: float = 1.0
    restricted_targets: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.max_rate <= 0:
            raise ValueError("max_rate must be positive")
        cleaned_actions = tuple(sorted({a.strip() for a in self.allowed_actions if a.strip()}))
        if not cleaned_actions:
            raise ValueError("allowed_actions cannot be empty")
        cleaned_restricted = tuple(sorted({t.strip() for t in self.restricted_targets if t.strip()}))
        object.__setattr__(self, "allowed_actions", cleaned_actions)
        object.__setattr__(self, "restricted_targets", cleaned_restricted)

    def is_action_allowed(self, action: str) -> bool:
        return action.strip() in self.allowed_actions

    def is_target_restricted(self, target: str) -> bool:
        return target.strip() in self.restricted_targets
