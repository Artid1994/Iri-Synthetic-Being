from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LearningExercise:
    question: str
    expected_answer: str
    verification_type: str = "EXACT"

    SUPPORTED_VERIFICATION_TYPES = {
        "EXACT",
        "NUMERICAL",
    }

    def __post_init__(self) -> None:
        if not self.question.strip():
            raise ValueError(
                "Learning exercise question cannot be empty"
            )

        if not self.expected_answer.strip():
            raise ValueError(
                "Learning exercise expected answer cannot be empty"
            )

        verification_type = self.verification_type.strip().upper()

        if verification_type not in self.SUPPORTED_VERIFICATION_TYPES:
            raise ValueError(
                "Invalid learning exercise verification type"
            )

        object.__setattr__(
            self,
            "verification_type",
            verification_type,
        )

    def verify(self, answer: str) -> bool:
        return answer.strip() == self.expected_answer.strip()
