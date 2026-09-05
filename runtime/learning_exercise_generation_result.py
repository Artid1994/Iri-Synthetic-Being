from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LearningExerciseGenerationResult:
    accepted: bool
    attempts: int
    reason: str

    def __post_init__(self) -> None:
        if self.attempts <= 0:
            raise ValueError(
                "Learning exercise generation attempts "
                "must be positive"
            )

        if not self.reason.strip():
            raise ValueError(
                "Learning exercise generation reason "
                "cannot be empty"
            )
