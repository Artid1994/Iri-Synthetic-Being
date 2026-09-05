from __future__ import annotations

from dataclasses import dataclass

from runtime.learning_exercise import LearningExercise


@dataclass(frozen=True)
class LearningVerificationResult:
    passed: bool
    reason: str


class LearningVerification:
    SUPPORTED_TYPES = {
        "EXACT",
        "NUMERICAL",
    }

    def check(
        self,
        exercise: LearningExercise | None,
        answer: str,
        verification_type: str = "EXACT",
        tolerance: float = 1e-6,
    ) -> LearningVerificationResult:
        verification_type = verification_type.strip().upper()

        if verification_type not in self.SUPPORTED_TYPES:
            return LearningVerificationResult(
                passed=False,
                reason="INVALID_VERIFICATION_TYPE",
            )

        if not isinstance(exercise, LearningExercise):
            return LearningVerificationResult(
                passed=False,
                reason="INVALID_EXERCISE",
            )

        if verification_type == "EXACT":
            passed = exercise.verify(answer)

        else:
            try:
                expected = float(exercise.expected_answer.strip())
                actual = float(answer.strip())
            except (TypeError, ValueError):
                return LearningVerificationResult(
                    passed=False,
                    reason="INVALID_NUMERICAL_ANSWER",
                )

            passed = abs(actual - expected) <= tolerance

        return LearningVerificationResult(
            passed=passed,
            reason=(
                "ANSWER_CORRECT"
                if passed
                else "ANSWER_INCORRECT"
            ),
        )
