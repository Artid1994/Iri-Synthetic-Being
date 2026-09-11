# Role / Purpose / Boundary Contract Session

## Overview
Phase 7 consolidates and explicitly decouples:
- Identity: "Who am I?" (developmental stage, accumulated experience, continuity).
- Role: "What am I doing?" (functional capacity, title/label).
- Purpose: "Why am I doing it?" (overarching rationale, declared intent).
- Goal: Specific objective state to achieve (priority, status: ACTIVE/PAUSED/COMPLETED).
- Intention: Specific executable action plan linking to a Goal (status: PENDING/ACTIVE/COMPLETED, `goal_id`).
- Safety Boundary: Constraint envelope (allowed actions, rate caps, restricted targets).

## Invariants
1. Never merge Role or Purpose into Identity.
2. Never treat Purpose as Goal (Purpose is enduring rationale; Goal is completable objective).
3. Never treat Goal as Intention (Goal is target; Intention is executable sub-act).
4. Safety Boundary is declarative and external; never confuse it with dynamic cognitive reasoning or autonomous execution.
5. None of these abstractions claim consciousness, sentience, or subjective experience.

## Implementation Pattern
```python
@dataclass(frozen=True)
class Role:
    name: str
    description: str = ""

@dataclass(frozen=True)
class Purpose:
    declaration: str
    rationale: str = ""

@dataclass(frozen=True)
class SafetyBoundary:
    allowed_actions: tuple[str, ...] = ("move", "respond")
    max_rate: float = 1.0
    restricted_targets: tuple[str, ...] = field(default_factory=tuple)
```
